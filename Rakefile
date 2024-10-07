directory "techies/refs/build"
file "techies/refs/build/game.html" => Dir["techies/refs/scaffold/*"] do
  chdir "techies/refs/scaffold" do
    ruby "build.rb"
  end
end

task default: "techies/refs/build/game.html"
