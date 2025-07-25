# feedback/hf_feedback.py

import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load model and tokenizer once
tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2")
model.eval()

def generate_feedback(task_name, action_log, score):
    bullet_summary = "\n".join(
        f"- {entry['hazard']}: {entry['action']} ({entry['reward']} / {entry['max_score']}, {'Correct' if entry['correct'] else 'Incorrect'})"
        for entry in action_log
    )

    prompt = f"""
You are a construction safety evaluator.

Task: {task_name}
Final Score: {score[0]} / {score[1]} → {score[2]}%
Action Summary:
{bullet_summary}

Generate a short and professional evaluation report with:
1. Summary
2. Strengths
3. Mistakes
4. Recommendations
5. Risk Awareness Score (1–10)

Report:
"""

    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        output_tokens = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

        generated = tokenizer.decode(output_tokens[0], skip_special_tokens=True)

        # Cut off the prompt from the output
        return generated[len(prompt):].strip()

    except Exception as e:
        return f"⚠️ Error generating feedback: {e}"
