# To compile

Follow these steps to compile the project locally:
- Clone the latest code from the remote branch
  > git clone https://github.com/kd-research/Techies.git
- Move to the root director
  > cd Techies
- Compile the code
  > pip install -e .

As long as no error appears, it means all the dependencies have been met, and the code is good to go!

# Setting environment variables

First, we need to make sure that all the required API keys are added to your environment variable. These include:
- [OpenAI API](https://openai.com/index/openai-api/) Key: For using openAI LLM models
  > export OPENAI_API_KEY=<\Your API Key>
- [Agentops AI](https://www.agentops.ai/) Key: For agents' monitoring, testing and debugging
  > export AGENTOPS_API_KEY=<\Your API Key>
- [Freesound API](https://freesound.org/apiv2/apply) Key: For downloading sound resources
  > export FREESOUND_CLIENT_API_KEY=<\Your API Key>
  
# To run

Follow these steps to run *Hierarch Crew* (game tree)  and/or *HTML Crew* (coding):
- Create a new working directory in the root and move there
  > mkdir working_dir
  > cd working_dir

## For Hierarchy Crew

- Use the following command to run the hierarchy crew
  > python ../techies/cli.py --ai `LLM_MODEL` run hierarchy_crew_v2 --game `GAME_SPECS`

  Here is a sample run:
  > python ../techies/cli.py --ai openai run hierarchy_crew_v2 --game Wordlenew_game_specifications
  
- You can choose an exisiting [game specification](https://github.com/kd-research/Techies/blob/main/techies/game_specs.py) or add a new one in the same file.
- The hierarchy crew will generate a game_hierarchy.xml (game tree file), in the current working directory (e.g., inside working_dir/)

## For HTML Crew

- Use the following command to run the HTML crew
  > python ../techies/cli.py --ai `LLM_MODEL` run html5_crew

  Here is a sample run:
  > python ../techies/cli.py --ai openai run html5_crew
  
- HTML crew assumes that there is a `game_hierarchy.xml` file exist in the current working directory (e.g., working_dir/game_hierarchy.xml).
- The HTML crew will generate a couple of files as output in the current working directory (E.g., inside working_dir/). These include:
  - index.html
  - style.css
  - script.js
  - game.html (combines `index.html`, `style.css`, and `script.js`)
  - *.mp3 (sounds files)
- You can run the game by either running `game.html` or `index.html`
