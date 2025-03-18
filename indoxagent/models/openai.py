from typing import List
from openai import OpenAI as OpenAIClient, AsyncOpenAI as AsyncOpenAIClient
from openai import APIConnectionError, APIStatusError, RateLimitError
from indoxagent.models.message import Message
from indoxagent.models.response import ModelResponse
from indoxagent.utils.log import logger


class OpenAI:
    """
    Handles communication with OpenAI models.
    """

    def __init__(self, api_key: str, model_id: str = "gpt-4"):
        self.api_key = api_key
        self.model_id = model_id
        self.client = OpenAIClient(api_key=self.api_key)
        self.async_client = AsyncOpenAIClient(api_key=self.api_key)

    def invoke(self, messages: List[dict]) -> ModelResponse:
        """
        Send a synchronous request to OpenAI.

        Args:
            messages (List[dict]): List of conversation messages.

        Returns:
            ModelResponse: Response from OpenAI.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages  # ✅ Fixed: No need for `.to_dict()`
            )
            if response.choices and response.choices[0].message:
                return ModelResponse(content=response.choices[0].message.content)
            return ModelResponse(content="Error: No response from OpenAI.")
        except RateLimitError as e:
            logger.error(f"Rate limit error: {e}")
            return ModelResponse(content="Error: Rate limit exceeded. Try again later.")
        except APIConnectionError as e:
            logger.error(f"Connection error: {e}")
            return ModelResponse(content="Error: Failed to connect to OpenAI API.")
        except APIStatusError as e:
            logger.error(f"API status error: {e}")
            return ModelResponse(content="Error: OpenAI API returned a status error.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return ModelResponse(content="Error: An unexpected issue occurred.")

    async def ainvoke(self, messages: List[dict]) -> ModelResponse:
        """
        Send an asynchronous request to OpenAI.

        Args:
            messages (List[dict]): List of conversation messages.

        Returns:
            ModelResponse: Response from OpenAI.
        """
        try:
            response = await self.async_client.chat.completions.create(
                model=self.model_id,
                messages=messages  # ✅ Fixed: No need for `.to_dict()`
            )
            if response.choices and response.choices[0].message:
                return ModelResponse(content=response.choices[0].message.content)
            return ModelResponse(content="Error: No response from OpenAI.")
        except RateLimitError as e:
            logger.error(f"Rate limit error: {e}")
            return ModelResponse(content="Error: Rate limit exceeded. Try again later.")
        except APIConnectionError as e:
            logger.error(f"Connection error: {e}")
            return ModelResponse(content="Error: Failed to connect to OpenAI API.")
        except APIStatusError as e:
            logger.error(f"API status error: {e}")
            return ModelResponse(content="Error: OpenAI API returned a status error.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return ModelResponse(content="Error: An unexpected issue occurred.")