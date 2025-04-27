import openai
from ....predefined_tools.base_tool import BaseTool, BaseModel, Field, Type, List, Dict, Any, os, requests, re
from bs4 import BeautifulSoup
from freesound import FreesoundClient


class SearchAndPickSoundToolSchema(BaseModel):
    """
    Defines the input arguments for performing a Freesound search
    and automatically picking one result in a single tool call.
    """
    description: str = Field(
        ...,
        description=(
            "Formatted query for Freesound API. For every term, you can use '+' and '-' "
            "modifier characters to indicate that a term is 'mandatory' or 'prohibited' "
            "(by default, terms are considered 'mandatory'). For example, in a query such "
            "as `term_a -term_b`, sounds including `term_b` will not match the search criteria. "
            "Avoid using the word 'sound' in the query unless necessary."
        )
    )
    output_path: str = Field(
        ...,
        description="Local file path where the chosen sound will be saved."
    )
    min_duration: int = Field(5, description="Minimum sound duration in seconds.")
    max_results: int = Field(8, description="Maximum number of results to fetch.")
    pick_instructions: str = Field(
        default="Pick the most interesting or relevant item.",
        description=(
            "A short piece of text or instructions to pass to the sub-LLM. "
            "It tells the LLM how to choose among the returned results."
        )
    )


class SearchAndPickSoundTool(BaseTool):
    """
    In a single call:
      - Searches Freesound for multiple results matching the query.
      - Invokes an LLM to pick the best match.
      - Downloads that chosen match to the specified path.
      - Returns JSON with info about all results and the chosen one.
    """
    name: str = "search_and_pick_sound"
    id: str = "search_and_pick_sound"
    description: str = (
        "Search Freesound with a single query, see multiple results, let an LLM choose one, "
        "then download the chosen result. Provide instructions for how to pick the best match."
    )
    args_schema: Type[BaseModel] = SearchAndPickSoundToolSchema

    def _run(self, **kwargs) -> Any:
        """
        Synchronous run. Gathers multiple search results, calls an LLM to decide,
        downloads the chosen sound, and returns JSON describing everything.
        """
        # Extract arguments
        description = kwargs["description"]
        output_path = kwargs["output_path"]
        min_duration = kwargs.get("duration", 5)
        max_results = min(kwargs.get("max_results", 6), 6)
        pick_instructions = kwargs.get("pick_instructions", "")

        if not description or not output_path:
            return "Missing required fields: 'description' and/or 'output_path'."

        # Check environment variables
        fs_token = os.environ.get("FREESOUND_CLIENT_API_KEY")
        if not fs_token:
            return "FREESOUND_CLIENT_API_KEY environment variable is not set."

        openai_api_key = os.environ.get("OPENAI_API_KEY")  # needed for sub-LLM call
        if not openai_api_key:
            return "OPENAI_API_KEY environment variable is not set."

        # ---- 1) FREESOUND SEARCH ----
        client = FreesoundClient()
        client.set_token(fs_token, "token")

        try:
            filter_str = f"duration:[{min_duration} TO *]"
            pager = client.text_search(query=description, filter=filter_str, fields="id,name,username,duration,description")
        except Exception as e:
            return f"Freesound search failed: {e}"

        # Collect results (with basic metadata)
        results = []
        for idx, sound in enumerate(pager):
            if idx >= max_results:
                break
            results.append({
                "index": idx,
                "id": sound.id,
                "name": sound.name,
                "username": sound.username,
                "description": sound.description[:150].strip() if sound.description else "N/A",
                "duration": sound.duration
            })

        if not results:
            return "No results found."

        # ---- 2) USE LLM TO PICK BEST ----
        # We'll feed the results + instructions into a small LLM prompt
        openai.api_key = openai_api_key

        # Build a short text prompt for the sub-LLM:
        prompt_text = (
            "We have a list of Freesound results, each has an `index`, `id`, `name`, `username`, and `duration`.\n\n"
            "Your goal: Decide which one to pick, based on the instructions:\n"
            f"'{pick_instructions}'\n\n"
            "Here are the search results:\n"
        )
        for r in results:
            prompt_text += (
                f"- index: {r['index']}, id: {r['id']}, name: {r['name']}, "
                f"uploader: {r['username']}, duration: {r['duration']:.1f} s\n"
            )
        prompt_text += (
            "\nReturn ONLY the index (as a number) of the best choice, nothing else.\n"
            "If uncertain, pick 0."
        )

        try:
            llm_response = openai.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "system", "content": "You choose the best sound from a list of sounds for a given scenario/request."},
                    {"role": "user", "content": prompt_text}
                ],
                # temperature=0.2,
                max_completion_tokens=20,
                n=1,
            )
            choice_text = llm_response.choices[0].message.content.strip()
        except Exception as e:
            return f"LLM call failed: {e}"

        # Attempt to parse the chosen index
        try:
            chosen_index = int(re.findall(r"\d+", choice_text)[0])
        except:
            chosen_index = 0

        if chosen_index < 0 or chosen_index >= len(results):
            chosen_index = 0  # fallback

        chosen_info = results[chosen_index]
        chosen_sound_id = chosen_info["id"]
        chosen_username = chosen_info["username"]

        # ---- 3) SCRAPE DESCRIPTION ----
        try:
            url = f"https://freesound.org/people/{chosen_username}/sounds/{chosen_sound_id}/"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            desc_section = soup.find(id="soundDescriptionSection")
            raw_desc = re.sub(r"<.*?>", "", str(desc_section)) if desc_section else ""
        except Exception:
            raw_desc = "N/A"

        # ---- 4) RETRIEVE SOUND PREVIEW ----
        # Need the full Sound object from Freesound
        chosen_sound = client.get_sound(chosen_sound_id)
        try:
            directory = os.path.dirname(output_path)
            filename = os.path.basename(output_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            chosen_sound.retrieve_preview(directory, filename)
        except Exception as e:
            return f"Failed to save sound (ID={chosen_sound_id}): {e}"

        # ---- 5) BUILD RESPONSE ----
        data = {
            "all_results": results,
            "llm_decision": choice_text,  # e.g., "Picked index 2"
            "chosen_index": chosen_index,
            "chosen_sound_id": chosen_sound_id,
            "chosen_sound_name": chosen_sound.name,
            "chosen_sound_description": raw_desc.strip(),
            "saved_path": output_path
        }
        import json
        return json.dumps(data, indent=2)

    async def _arun(self, **kwargs) -> Any:
        """Async version calls the same logic."""
        return self._run(**kwargs)