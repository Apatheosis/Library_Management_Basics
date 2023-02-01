# Library_Management_Basics
A very basic booking and inventory program for a place with excess books

Since I'm still a beginner the code shouldn't be too difficult to understand. Essentially, I'm saving the books and their data in one .csv file
and the users in another. Using pandas DataFrames as an intermediary between the .csv backend and the tkinter GUI, you can add, delete, borrow, 
and return books. It's still very much a work in progress but should you stumble across my humble github, feel free to just play around with it a little,
especially if you're still learing as well. 

Also be careful with special characters in book titles. I haven't configured the csv writer to ignore them yet so it could potentially break the base file.

