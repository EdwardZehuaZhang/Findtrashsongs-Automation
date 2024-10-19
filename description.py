import openai
import pandas as pd
import json


openai.api_key = "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"  # Replace this with your actual OpenAI API key


def generate_negative_critique(song_name, artist_name):
    prompt = f"""
    Write a negative song critique on {song_name} by {artist_name} in the following format:

    {song_name} - {artist_name} 
    space
    380 character critique
    space
    28 different hashtags
    
    Do not include any fluff when producing content. Each sentence should provide value to the overall goal of the content piece. Strictly follow this guideline. 

    My target audience are Instagram users. I am trying to create controversies. Keep this in mind and make sure critique has a clear negative tone.

    Make the content conversational, empathetic, sarcastic, and occasionally humorous. Use idioms, metaphors, anecdotes, and natural dialogue to add personality. But don't be Shakespeare.

    Incorporate internet slang words and musical technical jargons. Mention specific details such as progression, pacing, and others. 

    For hashtags, avoid generating random or meaningless tags like "hozierharmony" or "musicaljourney." Use simple, relevant words instead, and don't have to be negative, focus on maxmium engagement. For example, hashtags for "Beat It" by Michael Jackson could be #michaeljackson, #kingofpop, #beatit, or #nostalgicmusic. For "Somebody That I Used to Know" by Gotye, use tags like #gotye, #kimbra, #technomusic, or #technoremix. 

    Do generate without formating the text.
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a music critic."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        critique = response.choices[0].message.content.strip()
        return critique

    except Exception as e:
        print(f"Error generating critique: {e}")
        return None


def load_song_info(file_path='song_info.json'):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def run_description_pipeline():
    critique = generate_negative_critique(song_name, artist_name)
    
    if critique:
        with open("description.txt", "w", encoding="utf-8") as file:
            file.write(critique)
    
    return critique
    

if __name__ == "__main__":
    song_info = load_song_info()
    day = song_info['day']
    song_name = song_info['song_name']
    artist_name = song_info['artist_name']
    
    run_description_pipeline()
