# Key Concepts 📚

<!-- 
This section collects core concepts we use in our data engineering work. 
Each term is explained at three levels of depth (kid, teenager, tech lead) 
so that everyone in the team — from juniors to seniors — can build a shared understanding. 
-->

## Deterministic vs. Idempotent 🚀

This section explains two important concepts — **deterministic** and **idempotent** — in three levels of depth: like a kid 👶, like a teenager 👦, and like a technical lead 👨‍💻.

---

### 👶 As a 5-year-old

- **Deterministic**: Every time you press the same Lego button, you always get the **same toy** built 🧱.  
- **Idempotent**: When you clean up your toys, the room is clean. If you try to clean it again, nothing changes — it’s **still clean** 🧹.

---

### 👦 As a teenager

- **Deterministic**: Doing the same math equation with the same numbers always gives the **same result** ➕➖.  
- **Idempotent**: On Instagram, pressing the ❤️ once means you liked the post. Pressing it again doesn’t double it — it’s still **just one like** 👍.

---

### 👨‍💻 As a Technical Lead

- **Deterministic**: An operation is deterministic when the same input **always produces the same output**. In data pipelines, rerunning a job with the same source files should give identical results, with no randomness or order issues. ⚙️  
- **Idempotent**: An operation is idempotent when it can be **safely repeated** without changing the final state beyond the first run. In ETL, if we reprocess a file we already ingested, it should **not create duplicates** or corrupt data — the table remains correct. 🗄️

---

### 🎯 Quick cheat sheet

- **Deterministic** = Same input → same output (predictable).  
- **Idempotent** = Repeat the action → same final state (safe to retry).  
