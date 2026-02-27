# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Kevin** \
SUNet ID: **kevinsu** \
Citations: **Claude Code (Claude Opus 4.6) used as AI coding assistant for all exercises**

This assignment took me about **3** hours to do.


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt:
```
Analyze the existing extract_action_items() function in week2/app/services/extract.py. Implement an LLM-powered alternative extract_action_items_llm() that uses Ollama to extract action items from free-form text. Use structured outputs (Pydantic model with JSON schema) so the LLM returns a JSON object with an "items" array of strings. Use the llama3.2 model by default (configurable via OLLAMA_MODEL env var). Return an empty list for empty input without calling the LLM.
```

Generated Code Snippets:
```
week2/app/services/extract.py:10-11   – Added Pydantic BaseModel import and OLLAMA_MODEL config
week2/app/services/extract.py:92-126  – ActionItems schema and extract_action_items_llm() function
```

### Exercise 2: Add Unit Tests
Prompt:
```
Write unit tests for extract_action_items_llm() in week2/tests/test_extract.py. Cover: bullet list input, keyword-prefixed lines (TODO:/ACTION:), empty input (should return [] without calling LLM), no action items found, and prose paragraph input. Mock the ollama chat() call using unittest.mock.patch so tests run without a live Ollama server.
```

Generated Code Snippets:
```
week2/tests/test_extract.py:23-81 – 5 new test functions: test_llm_extract_bullet_list, test_llm_extract_keyword_prefixed, test_llm_extract_empty_input, test_llm_extract_no_action_items, test_llm_extract_prose_paragraph, plus _mock_ollama_response helper
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt:
```
Refactor the week2 backend for clarity: 1) Create Pydantic request/response schemas (NoteCreate, ExtractRequest, MarkDoneRequest, NoteResponse, ExtractResponse, ActionItemDetail, MarkDoneResponse) in a new schemas.py. 2) Update routers to use typed schemas instead of Dict[str, Any]. 3) Move init_db() into a FastAPI lifespan handler instead of module-level call. 4) Add proper error handling and response_model annotations to all endpoints.
```

Generated/Modified Code Snippets:
```
week2/app/schemas.py:1-43             – New file with all Pydantic request/response schemas
week2/app/main.py:1-34                – Refactored to use async lifespan for DB init, extracted FRONTEND_DIR constant
week2/app/routers/notes.py:1-42       – Replaced Dict[str, Any] with typed schemas, added response_model
week2/app/routers/action_items.py:1-82 – Replaced Dict[str, Any] with typed schemas, added response_model, added logging
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt:
```
1) Add a new POST /action-items/extract-llm endpoint that calls extract_action_items_llm() with error handling (return 502 on LLM failure). 2) Add a GET /notes endpoint that returns all saved notes. 3) Update the frontend: add an "Extract LLM" button next to Extract that calls /action-items/extract-llm, and a "List Notes" button that fetches and displays all notes from GET /notes.
```

Generated Code Snippets:
```
week2/app/routers/action_items.py:38-53  – POST /action-items/extract-llm endpoint
week2/app/routers/notes.py:35-42         – GET /notes endpoint
week2/frontend/index.html:28             – "Extract LLM" button
week2/frontend/index.html:34-35          – "List Notes" section and button
week2/frontend/index.html:42-54          – Shared doExtract() JS function for both buttons
week2/frontend/index.html:63-64          – Event listeners for Extract LLM button
week2/frontend/index.html:67-82          – List Notes fetch and render handler
```


### Exercise 5: Generate a README from the Codebase
Prompt:
```
Analyze the week2 codebase and generate a README.md with: project overview, directory structure, setup instructions (uv, Ollama model pull, running the server), API endpoints table for notes and action items, and how to run the test suite.
```

Generated Code Snippets:
```
week2/README.md:1-72 – Complete README with overview, project structure, setup, API table, and test instructions
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields.
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope.
