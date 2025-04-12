import json
import os
import re
import requests
from pydantic import BaseModel, Field
from typing import Type, List, Dict, Any, Optional, Union
from crewai.tools import BaseTool 