# Library Imports
import streamlit as st
from pathlib import Path
import pandas as pd
import os
import json
from dotenv import load_dotenv
from web3 import Web3
import odds_request


# Web 3 Connection
##########################################################################
# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('bet_slip_abi.json')) as f:
        bet_slip_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=bet_slip_abi
    )
    # Return the contract from the function
    return contract

# Load the contract
contract = load_contract()

# Python Code & Python Module Imports
################################################################################

# Import upcoming_games.csv
upcoming_games = pd.read_csv(Path("../Python_Modules/Resources/upcoming_games.csv"))
upcoming_games = upcoming_games.drop(columns="Unnamed: 0")

# Create games in CSV as individual variables.
# Could potentially create some sort of function for-loop that checks how many rows are in the upcoming_games.csv
# and returns that many Team variables.
Team_1 = f"{upcoming_games.iloc[0,2]} : {upcoming_games.iloc[0,3]}"
Team_2 = f"{upcoming_games.iloc[0,4]} : {upcoming_games.iloc[0,5]}"
Team_3 = f"{upcoming_games.iloc[1,2]} : {upcoming_games.iloc[1,3]}"
Team_4 = f"{upcoming_games.iloc[1,4]} : {upcoming_games.iloc[1,5]}"


# Streamlit Interface code.
##################################################################################

# Cover Image & Titles
st.image("./Footballfield.jpeg")
st.markdown('# SuperBowl Bet Machine')
st.markdown('## Current Week Matchups & Odds')

# Show current week betting options
st.dataframe(upcoming_games)

# Create form for submitting bet widgets
with st.form(key='place_bet'):
    st.markdown('### Place your bets here!')
    user_address = st.text_input('Enter your public address')
    user_name = st.text_input('Enter your UserName')
    user_bet_selection = st.selectbox('Choose YOUR winner:', [Team_1, Team_2, Team_3, Team_4])
    user_wager = st.number_input('Wager Amount', min_value=0)
    # Potential payout: We need to find a good way to take the odds from the bet selection and do the math to calculate the payout.
    # Probably an if statement. 
        # If odds are positive:
        # odds / 100 * wager = Potential payout
        # If odds are negative:
        # 100 / odds * wager = Potential payout
    potential_payout = st.text('Potential Payout Placeholder')
    # earned_payout will be 0 unless the bet wins and then it will equal potential_payout
    earned_payout = st.text('Earned Payout Placeholder')
    submitted = submit_button = st.form_submit_button(label='Submit Bet')
    if submitted:
        contract.functions.placeBet(user_address, user_name, user_bet_selection).transact({'from': user_address, 'value': w3.toWei(user_wager, 'ether'), 'gas':1000000})
        # def add_bet_info_to_df():
            # BET DF BODY
        
        # This can all be removed or refined so that it returns the bet information nicely.
        st.write(
            str(user_address),
            str(user_name),
            str(user_bet_selection),
            int(user_wager),
            # int(potential_payout),
            # int(earned_payout)
        )
        st.write("BetID")

# st.dataframe(placed_bets_df)

# Call block function. Checks to see if bet has finished.
st.sidebar.markdown('## Check Bet Status')
with st.sidebar.form(key="check_bet"):
    user_betID = st.text_input('Input your BetID')
    submitted = submit_button = st.form_submit_button(label='Check Bet Status')
    if submitted:
        st.write('Run check bet function')

# Payout bet form & function
st.sidebar.markdown('## Cash-In Winning Bet')
with st.sidebar.form(key="cash_bet"):
    user_betID = st.text_input('Input your BetID')
    submitted = submit_button = st.form_submit_button(label='Cash Bet')
    if submitted:
        st.write('Run cash bet function')