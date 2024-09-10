require "bundler/setup"

Bundler.require

require "slim/include"


Slim::Engine.set_options pretty: true
# temple = Tilt.new("game.html.slim")
src = File.join(__dir__, "game.html.slim")
dest = File.join(__dir__, "../build/game.html")
temple = Slim::Template.new(src)
File.write(dest, temple.render)
