map_template = """
Please summarise the following text in a concise and coherent way, ensuring
that you capture the main points of the text.

Text: {docs}
Summary: 
"""

reduce_template = """
The following is set of summaries:
{docs}

Take these and distill it into a final, consolidated summary of the main themes. 
Helpful Answer:
"""
