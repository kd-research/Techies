{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";

  };

  outputs =
    inputs@{ nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        shellScript = pkgs.writeShellScriptBin "python-wrapper" ''
          export LD_LIBRARY_PATH="${
            pkgs.lib.makeLibraryPath [
              pkgs.stdenv.cc.cc.lib
              pkgs.zlib
            ]
          }:$LD_LIBRARY_PATH"

          exec uv run python "$@"
        '';

        python-wrapper = pkgs.stdenv.mkDerivation {
          name = "python-wrapper";
          phases = [ "installPhase" ];
          buildInputs = with pkgs; [
            shellScript
            python312
            uv
          ];
          installPhase = ''
            mkdir -p $out/bin
            ln -s ${shellScript}/bin/python-wrapper $out/bin
          '';
        };
      in
      {

        apps = rec {
          python = {
            type = "app";
            program = "${python-wrapper}/bin/python-wrapper";
          };
          default = python;
        };

        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            python312
            python312Packages.numpy
            uv
          ];
        };
      }
    );
}
