import streamlit_authenticator as stauth

passwords = ["gabi692", "luana692"]

hashed_passwords = stauth.Hasher(passwords=passwords).generate()

print(hashed_passwords)
