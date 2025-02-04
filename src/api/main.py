from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.compiler.lexer import Lexer, Token, TokenType

app = FastAPI(title="GenomeScript API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str

class TokenResponse(BaseModel):
    line: int
    column: int
    type: str
    value: str

@app.get("/")
async def root():
    return {"message": "GenomeScript API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze_code(request: CodeRequest):
    try:
        lexer = Lexer(request.code)
        tokens = lexer.tokenize()
        
        # Convert tokens to response format
        token_list = [
            {
                "line": token.line,
                "column": token.column,
                "type": token.type.name,
                "value": token.value
            }
            for token in tokens if token.type != TokenType.EOF
        ]
        
        return {"tokens": token_list}
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))