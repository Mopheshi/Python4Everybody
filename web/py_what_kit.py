import pywhatkit as kt

# Send a WhatsApp message
target_number = "+2348186116002"  # Recipient's phone number
message = "Hello, this is a test message!"
kt.sendwhatmsg(target_number, message, 5, 30)  # Sends the message after 5 seconds

# Perform a Google search
search_query = "https://play.google.com/store/apps/details?id=morpheus.softwares.hbadictionary"
kt.search(search_query)
