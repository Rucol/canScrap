from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging
import time

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Wykrywanie urządzenia (GPU, jeśli dostępne)
device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Urządzenie: {device}")

# 🔹 Ścieżka do modelu Mistral (zmień na swoją)
MODEL_PATH = "D:/Mistral/mistral-7B-v0.1"

# Załadowanie modelu i tokenizera
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    tokenizer.pad_token = tokenizer.eos_token  # 🔹 Ustawienie brakującego tokena
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    ).to(device)
    logger.info("Model i tokenizer zostały pomyślnie załadowane.")
except Exception as e:
    logger.error(f"Błąd podczas ładowania modelu: {e}")
    raise

class Request(BaseModel):
    prompt: str
    max_tokens: int = 200

@app.post("/generate/")
async def generate_text(request: Request):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt nie może być pusty.")

    if request.max_tokens <= 0 or request.max_tokens > 1024:
        raise HTTPException(status_code=400, detail="max_tokens musi być między 1 a 1024.")

    try:
        start_time = time.time()
        inputs = tokenizer(request.prompt, return_tensors="pt").to(device)
        logger.info(f"Liczba tokenów w prompt: {inputs.input_ids.shape[1]}")    

        with torch.inference_mode():  #  Poprawna obsługa inference
            output = model.generate(
    **inputs,
    max_new_tokens=request.max_tokens,
    temperature=0.3,
    top_p=0.6,
    repetition_penalty=1.2,
    pad_token_id=tokenizer.eos_token_id
)


        #  Usunięcie powtórzonego promptu w odpowiedzi
        logger.info(f"Odpowiedź modelu (przed dekodowaniem): {output}")
        response_text = tokenizer.decode(output[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)


        end_time = time.time()
        logger.info(f"Czas generowania: {end_time - start_time:.2f} sekund")

        return {"response": response_text}

    except Exception as e:
        logger.error(f"Błąd generowania: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Błąd generowania: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
