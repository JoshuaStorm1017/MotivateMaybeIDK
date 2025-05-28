import streamlit as st
from datetime import datetime, time, timedelta
import random
import secrets

# ————— Constants —————
QUOTES = [
    "Teamwork: because none of us is as dumb as all of us.",
    "Hard work pays off eventually, but laziness pays off right now.",
    "Always remember you're unique, just like everyone else.",
    "Aim low, avoid disappointment.",
    "Dream small, it's cheaper.",
    "The road to success is always under construction—better stay home.",
    "If at first you don't succeed, redefine success.",
    "Believe in yourself, because the rest of us think you're an idiot.",
    "Mistakes are proof that you're trying... and failing spectacularly.",
    "Give 100% at work: 15% on Monday, 20% on Tuesday, tapering off gradually.",
    "Every dead body on Mount Everest was once a highly motivated person.",
    "Procrastination: Why do today what you can panic about tomorrow?",
    "Always follow your dreams. Except the weird ones, nobody wants to hear about those.",
    "When life gives you lemons, complain loudly until someone gives you chocolate.",
    "You didn't come this far only to come this far—unless this is good enough.",
    "If you think nobody cares if you're alive, try missing a couple of payments.",
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "Remember, there's no 'I' in team, but there's definitely 'me.'",
    "Success is just failure that hasn't happened yet.",
    "Keep your dreams alive—hit snooze repeatedly.",
    "Shoot for the moon. If you miss, you’ll land among the unpaid interns.",
    "Don’t stop believing—unless it gets inconvenient.",
    "Work smarter, not harder. Or ideally, not at all.",
    "You miss 100% of the naps you don’t take.",
    "Be yourself. Unless you suck, then maybe don't.",
    "Failure is not an option—it’s standard procedure.",
    "Rise and grind? More like snooze and whine.",
    "One day you'll look back on this and laugh... nervously, while filing bankruptcy.",
    "Why try and fail when you can not try and chill?",
    "The journey of a thousand miles begins with a bad GPS signal.",
    "Strive for progress, not perfection—and still give up halfway.",
    "Good things come to those who wait… or to those with rich parents.",
    "If opportunity doesn’t knock, just blame the economy.",
    "The glass is half full… of disappointment.",
    "Do one thing every day that scares you—like checking your bank account.",
    "Your vibe attracts your tribe, unless you're annoying.",
    "Everything happens for a reason. Sometimes that reason is you're dumb.",
    "Go the extra mile. It's empty and no one will see you fail.",
    "Stay positive, test negative, and remain mediocre.",
    "You're never too old to give up on your dreams.",
    "Hustle in silence… so no one hears you crash and burn.",
    "It’s not about the destination. It’s about how lost you get along the way.",
    "Turn your wounds into wisdom—or just more trauma, whichever comes first.",
    "Remember: even a broken clock is right twice a day. You're not even trying that hard.",
    "Be the change you wish to see in the world—or just tweet angrily from your couch.",
]

WORK_START = time(8, 30)
WORK_END   = time(18, 0)

# ————— Page config & auto-refresh —————
st.set_page_config(page_title="Workday Progress", layout="centered")
st.markdown('<meta http-equiv="refresh" content="60">', unsafe_allow_html=True)

OFFSET_HOURS = -4  # change to -5 if you need a 5-hour shift

def now() -> datetime:
    # take UTC and shift by OFFSET_HOURS to match your local
    return datetime.utcnow() + timedelta(hours=OFFSET_HOURS)

def progress_percent(current: datetime) -> float:
    today     = current.date()
    start_dt  = datetime.combine(today, WORK_START)
    end_dt    = datetime.combine(today, WORK_END)
    if current <= start_dt:
        return 0.0
    if current >= end_dt:
        return 100.0
    total_secs   = (end_dt - start_dt).total_seconds()
    elapsed_secs = (current - start_dt).total_seconds()
    return (elapsed_secs / total_secs) * 100

def random_quote() -> str:
    return secrets.choice(QUOTES)

# ————— Gather data —————
current       = now()
pct_float     = progress_percent(current)
pct_int       = int(pct_float)
time_str      = current.strftime("%I:%M %p")
start_str     = WORK_START.strftime("%I:%M %p")
end_str       = WORK_END.strftime("%I:%M %p")
quote         = random_quote()

# ————— Layout —————
st.title("📊 Workday Progress")
st.markdown(f"**Work hours:** {start_str} → {end_str}")

# Two-column metrics
col1, col2 = st.columns(2)
col1.metric("⏰ Current Time", time_str)
col2.metric("📈 Completion", f"{pct_float:.1f}%")

st.markdown("---")

# New section as requested
st.subheader(f"🚀 Towards {end_str}")
st.progress(pct_int)
st.write(f"You are **{pct_float:.1f}%** through your workday ({start_str} - {end_str}).")

# Contextual messages
if pct_int == 0 and current.time() < WORK_START:
    st.info("The workday hasn't started yet. Enjoy the calm before the storm!")
elif pct_int == 100 and current.time() >= WORK_END:
    st.success("🎉 Workday complete! Time to escape... or start your second job.")
elif 0 < pct_float < 30:
    st.info("Just getting started... The coffee is still warm (maybe).")
elif 30 <= pct_float < 70:
    st.warning("Deep in the trenches. Keep pushing (or find a good hiding spot).")
else:  # 70–99.9
    st.info("Almost there! The finish line is in sight... or is that another meeting invitation?")

st.markdown("---")
st.markdown(f"> _{quote}_")
