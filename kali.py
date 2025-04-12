import subprocess
import openai

# OpenAI API anahtarınızı buraya ekleyin
openai.api_key = "YOUR_API_KEY"

def shell_ai():
    print("İSH AI'ye hoş geldiniz! Çıkmak için 'exit' yazın.")
    while True:
        # Kullanıcıdan komut al
        user_input = input("Komutunuzu yazın: ")

        if user_input.lower() == "exit":
            print("Çıkış yapılıyor...")
            break

        try:
            # OpenAI ile NLP işleme
            completion = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Kullanıcı komutu: {user_input}\nBu komutu yorumla ve uygun bir shell komutu öner:",
                max_tokens=50
            )
            ai_response = completion.choices[0].text.strip()

            print(f"AI Yorumladı: {ai_response}")

            # Yorumlanmış komutu çalıştır
            process = subprocess.Popen(ai_response, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()

            if output:
                print("Çıktı:\n", output.decode())
            if error:
                print("Hata:\n", error.decode())

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    shell_ai()