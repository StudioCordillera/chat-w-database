raw_data = """Need to have 10 user manuals recreated in vector format. You&#039;ll be provided with scans of the originals. They are all mostly text with some line drawings. We&#039;ll need you to recreate all line drawings in vector format as well as re-type and/or reformat the text sections. Each booklet/brochure is a different size and shape, which you&#039;ll need to match. Colors, typefaces, and logos will need to match the originals. No bleed required. We&#039;ll want to get the files back as editable InDesign or Illustrator files with all fonts and images included.<br /><br />
Some of them are trifold brochures, some are booklets, some are inserts. We need this done in two weeks. We need them prepped and ready to print directly from the files you send us. Please don&#039;t apply for this project if you are unfamiliar with best printing practices.<br /><br />
We&#039;ve attached one of the manuals for reference. They are not all exactly like this, but this is pretty typical of the 10 we need recreated.<br /><br /><b>Hourly Range</b>: $25.00-$30.00

<br /><b>Posted On</b>: May 22, 2023 16:01 UTC<br /><b>Category</b>: Illustration<br /><b>Skills</b>:Graphic Design,     Adobe Illustrator,     Adobe Photoshop,     Instruction Manual,     Layout Design,     Adobe InDesign,     Illustration,     User Manual,     English,     Technical Documentation    
<br /><b>Country</b>: United States
<br /><a href="https://www.upwork.com/jobs/Recreate-User-Manuals_%7E01147e92c97c9a6dde?source=rss">click to apply</a>"""

# Replace HTML entities with their corresponding characters
clean_data = raw_data.replace("&#039;", "'")

# Write the cleaned data to a .txt file
with open("cleaned_data.txt", "w") as file:
    file.write(clean_data)

print("<a href='/download?file=cleaned_data.txt'>Download file</a>")