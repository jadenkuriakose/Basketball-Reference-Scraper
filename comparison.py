import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests as req
from bs4 import BeautifulSoup

def construct_url(first_name, last_name):
    base = "https://www.basketball-reference.com"
    initial1 = f"/players/{last_name[0].lower()}/{last_name.lower()[:5]}{first_name.lower()[0:2]}01.html"
    url1 = base + initial1
    return url1

def extract_stats(url):
    try:
        response = req.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        stats_pullout = soup.find('div', class_='stats_pullout')
        
        if stats_pullout:
            stats = {}
            for span in stats_pullout.find_all('span', {'data-tip': True}):
                data_tip = span.get('data-tip')
                p_tag = span.find_next_sibling('p')
                while p_tag:
                    value = p_tag.text.strip()
                    if value.replace('.', '', 1).isdigit():
                        if data_tip in ["Points", "Total Rebounds", "Assists"]:
                            stats[data_tip] = value
                        break
                    p_tag = p_tag.find_next_sibling('p')
            return stats
        return None

    except req.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def fetch_player_stats(first_name, last_name):
    url = construct_url(first_name, last_name)
    return extract_stats(url)

def compare_players():
    first_name1 = first_name_entry1.get()
    last_name1 = last_name_entry1.get()
    first_name2 = first_name_entry2.get()
    last_name2 = last_name_entry2.get()
    
    if not (first_name1 and last_name1 and first_name2 and last_name2):
        messagebox.showwarning("Input Error", "Please enter names for both players.")
        return
    
    stats_player1 = fetch_player_stats(first_name1, last_name1)
    stats_player2 = fetch_player_stats(first_name2, last_name2)
    
    if stats_player1 is None or stats_player2 is None:
        messagebox.showinfo("No Data", "No statistics found for one or both players.")
        return
    
    compare_stats(stats_player1, stats_player2, first_name1, last_name1, first_name2, last_name2)

def compare_stats(stats1, stats2, first_name1, last_name1, first_name2, last_name2):
    comparison_text = f"Comparing {first_name1} {last_name1} and {first_name2} {last_name2}:\n\n"
    ordered_stats = ["Points", "Total Rebounds", "Assists"]
    
    for stat in ordered_stats:
        value1 = stats1.get(stat, "N/A")
        value2 = stats2.get(stat, "N/A")
        comparison_text += f"{stat}:\n  {first_name1} {last_name1}: {value1}\n  {first_name2} {last_name2}: {value2}\n\n"
    
    stats_text.delete('1.0', tk.END)  
    stats_text.insert(tk.END, comparison_text)

root = tk.Tk()
root.title("NBA Player Stats Comparison")
root.geometry("600x500")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Player 1 First Name:", font=("Arial", 12), bg="#1e1e1e", fg="#ffffff").grid(row=0, column=0, pady=5, padx=5, sticky='e')
first_name_entry1 = tk.Entry(input_frame, font=("Arial", 12))
first_name_entry1.grid(row=0, column=1, pady=5, padx=5)

tk.Label(input_frame, text="Player 1 Last Name:", font=("Arial", 12), bg="#1e1e1e", fg="#ffffff").grid(row=1, column=0, pady=5, padx=5, sticky='e')
last_name_entry1 = tk.Entry(input_frame, font=("Arial", 12))
last_name_entry1.grid(row=1, column=1, pady=5, padx=5)

tk.Label(input_frame, text="Player 2 First Name:", font=("Arial", 12), bg="#1e1e1e", fg="#ffffff").grid(row=2, column=0, pady=5, padx=5, sticky='e')
first_name_entry2 = tk.Entry(input_frame, font=("Arial", 12))
first_name_entry2.grid(row=2, column=1, pady=5, padx=5)

tk.Label(input_frame, text="Player 2 Last Name:", font=("Arial", 12), bg="#1e1e1e", fg="#ffffff").grid(row=3, column=0, pady=5, padx=5, sticky='e')
last_name_entry2 = tk.Entry(input_frame, font=("Arial", 12))
last_name_entry2.grid(row=3, column=1, pady=5, padx=5)

compare_button = tk.Button(root, text="Compare Stats", font=("Arial", 12), command=compare_players, bg="#4CAF50", fg="white")
compare_button.pack(pady=10)

stats_text = scrolledtext.ScrolledText(root, width=70, height=15, font=("Arial", 12), bg="#2e2e2e", fg="#ffffff")
stats_text.pack(pady=10)

root.mainloop()
