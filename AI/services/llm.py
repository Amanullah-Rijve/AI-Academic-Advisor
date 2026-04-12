from openai import OpenAI

client = OpenAI(api_key="")

def ask_llm(context,question,student):
    prompt = f'''
    You are an AI Advisor.
    
    Student:
    Semseter:{student['semester']}
    Department:{student['department']}
    
    Context: {context}
    
    Question:{question}
    
    '''
    
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content