import tkinter as tk
from tkinter import messagebox
import random

# Save eliminated or final winner
def save_result(name):
    with open("final_winners.txt", "a") as f:
        f.write(f"{name}\n")

# Animate the counting
def animate_counting(count_step, label, callback):
    label.config(text="🔢 Counting:\n")
    label.update()

    def count(i=1):
        if i <= count_step:
            label.config(text=label.cget("text") + f"{i}...\n")
            label.update()
            root.after(300, count, i + 1)
        else:
            callback()

    count()

# Eliminate one item based on random count
def eliminate_one(finalists, label):
    if len(finalists) == 1:
        winner = finalists[0]
        messagebox.showinfo("🏆 Game Over", f"The final winner is:\n\n{winner}")
        label.config(text=f"🏁 Final Winner: {winner}")
        save_result(winner)
        return

    count_step = random.choice([5, 10])
    label.config(text=f"🔁 Random Count Used: {count_step}\n")
    label.update()

    def after_count():
        index = (count_step - 1) % len(finalists)
        eliminated = finalists.pop(index)
        label.config(text=label.cget("text") + f"❌ Eliminated: {eliminated}\n\n")
        label.config(text=label.cget("text") + f"✅ Remaining: {', '.join(finalists)}")
        save_result(eliminated)
        root.after(1500, lambda: eliminate_one(finalists, label))

    animate_counting(count_step, label, after_count)

# Start the game
def start_game():
    friends = entry_friends.get().strip().split(",")
    dreams = entry_dreams.get().strip().split(",")
    ranks = entry_ranks.get().strip().split(",")
    extras = entry_extras.get().strip().split(",")

    # Validate input
    if len(friends) != 3 or len(dreams) != 3 or len(ranks) != 3 or len(extras) != 3:
        messagebox.showwarning("❗ Input Error", "Please enter exactly 3 items for each category, separated by commas.")
        return

    # Tag each item
    friend_list = [f.strip() + " (Friend)" for f in friends]
    dream_list = [d.strip() + " (Dream)" for d in dreams]
    rank_list = [r.strip() + " (Rank)" for r in ranks]
    extra_list = [e.strip() + " (Bonus)" for e in extras]

    finalists = friend_list + dream_list + rank_list + extra_list
    eliminate_one(finalists, output_label)

# Reset the form
def reset_game():
    entry_friends.delete(0, tk.END)
    entry_dreams.delete(0, tk.END)
    entry_ranks.delete(0, tk.END)
    entry_extras.delete(0, tk.END)
    output_label.config(text="")

# GUI Setup
root = tk.Tk()
root.title("🎮 Kiran's Elimination Game")
root.geometry("600x600")
root.configure(bg="#f0f8ff")

# Labels and Entry Fields
tk.Label(root, text="👬 Best Friends (3, comma separated):", bg="#f0f8ff").pack()
entry_friends = tk.Entry(root, width=50)
entry_friends.pack()

tk.Label(root, text="🌟 Childhood Dreams (3, comma separated):", bg="#f0f8ff").pack()
entry_dreams = tk.Entry(root, width=50)
entry_dreams.pack()

tk.Label(root, text="🥇 Ranks (3, comma separated):", bg="#f0f8ff").pack()
entry_ranks = tk.Entry(root, width=50)
entry_ranks.pack()

tk.Label(root, text="🎁 Extras (3, comma separated):", bg="#f0f8ff").pack()
entry_extras = tk.Entry(root, width=50)
entry_extras.pack()

# Buttons
tk.Button(root, text="▶️ Start Game", command=start_game, bg="#4CAF50", fg="white", width=25).pack(pady=10)
tk.Button(root, text="🔁 Reset", command=reset_game, bg="#2196F3", fg="white", width=25).pack()

# Output Label
output_label = tk.Label(root, text="", justify="left", bg="#f0f8ff", fg="black", font=("Courier", 10))
output_label.pack(pady=20)

root.mainloop()
