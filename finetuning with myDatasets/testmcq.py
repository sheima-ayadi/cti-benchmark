import pandas as pd

def extract(model_output:str)-> str:
    end_of_text = model_output.find("<|end_of_text|>")
    #return first english alphabet chracter before end_of_text
    answer = model_output[:end_of_text]
    answer = answer[::-1]

    for x in answer:
        if 'A' <= x.upper() <= 'Z':
            return x.upper()
    return ""

def evaluate_model(path:str)-> float:
    #take the answer as the first alphabet character just before <|end_of_text|> in df['model_outputs']
    df = pd.read_csv(path)
    # #use "model_outputs" to extract answer and compare it to "output"
    correct = 0
    for i in range(len(df)):
        correct_output = df.iloc[i]['output']
        model_output = extract(df.iloc[i]['model_outputs'])
        print(model_output, correct_output)
        if correct_output == model_output:
            correct+=1
    return correct / len(df) * 100


path = "our-cti-mcq-with-model-outputs.csv" #change it
result = evaluate_model(path = path)

print(result)