import json
import os
from typing import Optional

# Custom exceptions for knowledge base errors
class KnowledgeBaseError(Exception):
    def __init__(self, message="Knowledge base error occurred"):
        super().__init__(message)

class KnowledgeBaseFileError(KnowledgeBaseError):
    def __init__(self, message="Knowledge base file error"):
        super().__init__(message)

class KnowledgeBaseDataError(KnowledgeBaseError):
    def __init__(self, message="Knowledge base data error"):
        super().__init__(message)

class EntryNotFoundError(KnowledgeBaseError):
    def __init__(self, message="No entry found"):
        super().__init__(message)

class InvalidQueryError(KnowledgeBaseError):
    def __init__(self, message="Invalid query"):
        super().__init__(message)

def _validate_query(query: str) -> str:
    if not isinstance(query, str):
        raise InvalidQueryError("Query must be a string")
    
    if not query or not query.strip():
        raise InvalidQueryError("Query cannot be empty")
    
    return query.strip()

def _load_knowledge_base() -> dict:
    kb_path = "data/kb.json"
    
    if not os.path.exists(kb_path):
        raise KnowledgeBaseFileError(f"Knowledge base file not found: {kb_path}")
    
    try:
        with open(kb_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise KnowledgeBaseDataError(f"Invalid JSON in knowledge base: {e}")
    except IOError as e:
        raise KnowledgeBaseFileError(f"Cannot read knowledge base file: {e}")
    
    if not isinstance(data, dict):
        raise KnowledgeBaseDataError("Knowledge base must be a JSON object")
    
    if "entries" not in data:
        raise KnowledgeBaseDataError("Knowledge base missing 'entries' field")
    
    if not isinstance(data["entries"], list):
        raise KnowledgeBaseDataError("Knowledge base 'entries' must be a list")
    
    return data

def _search_entries(query: str, entries: list) -> Optional[str]:
    query_lower = query.lower()
    
    for entry in entries:
        if not isinstance(entry, dict):
            continue
            
        name = entry.get("name", "")
        if isinstance(name, str) and name.lower() == query_lower:
            return entry.get("summary", "No summary available")
    
    for entry in entries:
        if not isinstance(entry, dict):
            continue
            
        name = entry.get("name", "")
        if isinstance(name, str) and query_lower in name.lower():
            return entry.get("summary", "No summary available")
    
    return None

def kb_lookup(query: str) -> str:

    try:
       
        validated_query = _validate_query(query)
        
       
        kb_data = _load_knowledge_base()
        

        result = _search_entries(validated_query, kb_data["entries"])
        
        if result is None:
            available_entries = []
            for entry in kb_data["entries"]:
                if isinstance(entry, dict) and "name" in entry:
                    available_entries.append(entry["name"])
            
            if available_entries:
                available_list = ", ".join(sorted(available_entries))
                raise EntryNotFoundError(
                    f"No entry found for '{query}'."
                )
            else:
                raise EntryNotFoundError(f"No entry found for '{query}' and knowledge base is empty")
        
        return result
        
    except (InvalidQueryError, KnowledgeBaseFileError, KnowledgeBaseDataError, EntryNotFoundError) as e:
        raise e
    except Exception as e:
        raise KnowledgeBaseError(f"Unexpected knowledge base error: {str(e)}")
