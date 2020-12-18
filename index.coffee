# Executing the script, everything written by the script will be stored in the variable output
command: 'python3 covid-tracker/covid.py'

# Refreshing data every hour
refreshFrequency: '3600s'

# Creating the widget
update: (output, domEl) ->
    $(domEl).empty().append("#{output}")

# Styling
style: """

// Position of the widget
margin: 0px
right: 10px
bottom: 10px

// Border arount table
table {
	border: 1px solid black;
}

// Styles all columns except the first one
td + td {
	text-align:center;
}

"""
