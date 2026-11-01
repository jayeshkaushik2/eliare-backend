from app.schemas.logs_schema import ErrorStatuses
from google import genai
from settings import settings
from enum import Enum

class AiAvailable(Enum):
    GEMINI = "gemini"
    CLAUDE = "claude"
    CHATGPT = "chatgpt"

# TODO need to make below store empty, currently set only for testing
AI = {AiAvailable.gemini.value: None}
AI_MODELS = {AiAvailable.gemini.value: ["gemini-flash-latest"]}

if settings.GEMINI_API_KEY:
    gemini = genai.Client(api_key=settings.GEMINI_API_KEY)
    AI[AiAvailable.gemini.value] = gemini
    AI_MODELS[AiAvailable.gemini.value] = ["gemini-flash-latest"]

# TODO To be added in future for better results
if settings.CLAUDE_API_KEY:
    AI[AiAvailable.CLAUDE] = None

class Agent:
    def __init__(self, ai: str, model: str):
        if ai not in AI:
            raise ValueError(f"Invalid AI name {ai}, options are {AI.keys()}")
        
        models = AI_MODELS[ai]
        if model not in models:
            raise ValueError(f"Invalid AI model name {model}, options are {models}")

        self.ai_name = ai
        self.ai = AI[ai]
        self.model = model
        print(f"AI {self.ai} selected, with model name {self.model}")

    def gen_context(self, *args, **kwargs):
        return """Act as a expert software engineer with deep knowledge of Python, Django, and Problem solving.

## I want you to analize the production log/issue occurred at {error_dt}:
    - Issue message: {message}
    - Issue error_json/details: {error_json}


## Once the issue is analized, find out the root cause of this issue at repositary {repositary_path}, once the root cause is found find out an opmitmal and minimal fix for it. Once the fix is written if possible try to check that fix with the same use case which got failed. if the use case is passed and the fix is working create a new branch in format "autofix/<fix_branchname>-<datetime of fix>" .

## Raise the new pull request for this branch to parent branch ("master" branch), in commit message add below details:
    - Issue LOG_ID: {error_log_id}.
    - Issue use case which got failed, and why?
    - What fix was done?
    - Time and Space complexcity before and after the fix?
    - (Optional) What other part of the code we can fix as well?

Rules:
    0. Before finding the root cause always make sure the branch is "master".
    1. Do not change the base line logic of the code.
    2. Do not try to create extra files for small changes.
    3. Do not add multiple comments, use very minimal and to the point comments only which are necessary."""

    def fix_log_error(self, error_log):
        error_dt = error_log.error_dt
        message = error_log.message
        error_json = error_log.error_json
        repositary_path = "/code"
        error_log_id = error_log._id

        # generating context
        context = self.gen_context().format(
            error_dt,
            message,
            error_json,
            repositary_path,
            error_log_id,
        )
        print(f"Context generated: {context}")
        return 
        # TODO need to use below code later, while testing
        response = client.models.generate_content(
            model=self.model,
            contents={'text': context}
        )
        return response