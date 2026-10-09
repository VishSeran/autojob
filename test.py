# from database.session import DB_Session
# from repositories.user_repository import UserRepository


# db = DB_Session()

# repo = UserRepository(db)

# user = repo.create(
#     email="seran@gmail.com",
#     name="Seran Vishwa"
# )

# print(user.id)
# print(user.email)

# found_user = repo.get_by_email(
#     "seran@gmail.com"
# )

# # delete_user = repo.delete_user(found_user)

# print(found_user)

# db.close()

# from cryptography.fernet import Fernet

# print(
#     Fernet.generate_key().decode()
# )

from services.encryption_service import EncryptionService


encryption = EncryptionService()

value = "I am here to find a solution to Autojob"
print(value)

encrypted_value = encryption.encrypt(value)
print(f"\nencrypted_value: {encrypted_value}")

decrypted_value = encryption.decrypt(encrypted_value)
print(f"\ndecrypted_value: {decrypted_value}")