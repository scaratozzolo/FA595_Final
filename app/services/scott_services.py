import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, AutoModelForCausalLM, AutoTokenizer

GPTtokenizer = GPT2Tokenizer.from_pretrained("gpt2")
GPTmodel = GPT2LMHeadModel.from_pretrained("gpt2")

DialoGPTtokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
DialoGPTmodel = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def next_word(text, k=5):

    indexed_tokens = GPTtokenizer.encode(text)
    tokens_tensor = torch.tensor([indexed_tokens])
    tokens_tensor = tokens_tensor.to(device)
    GPTmodel.to(device)

    with torch.no_grad():
        outputs = GPTmodel(tokens_tensor)
        predictions = outputs[0]

    probs = predictions[0, -1, :]
    top_next = [GPTtokenizer.decode(i.item()).strip() for i in probs.topk(k)[1]]

    return {"predicted_words": top_next}

chat_history = {0:"Placeholder"}

def chat_bot(text, chat_id=None):

    global chat_history

    if chat_id is not None:
        try:
            chat_history[chat_id]
        except:
            return {"error": f"chat_id does not exist. given: {chat_id}"}

    new_user_input_ids = DialoGPTtokenizer.encode(text + DialoGPTtokenizer.eos_token, return_tensors='pt')

    bot_input_ids = torch.cat([chat_history[chat_id], new_user_input_ids], dim=-1) if chat_id != None else new_user_input_ids

    if chat_id == None:
        chat_id = max(chat_history.keys())+1

    chat_history[chat_id] = DialoGPTmodel.generate(bot_input_ids, max_length=1000, pad_token_id=DialoGPTtokenizer.eos_token_id)

    output = DialoGPTtokenizer.decode(chat_history[chat_id][:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return {"response": output, "chat_id": chat_id}

if __name__ == '__main__':

    print(chat_bot("Elon Musk is my favorite"))
    print(chat_bot("Why not?", 1))
    print(chat_bot("Do you not like cars?", 1))

