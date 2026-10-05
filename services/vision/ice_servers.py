import os
import logging
import streamlit as st

logger = logging.getLogger(__name__)

FALLBACK_ICE_SERVERS = [{"urls": ["stun:stun.l.google.com:19302"]}]


def _read_secret(name):
    value = os.environ.get(name, "")
    if value:
        return value
    try:
        return st.secrets.get(name, "")
    except Exception:
        return ""


@st.cache_data(ttl=3600, show_spinner=False)
def get_ice_servers():
    """Return TURN/STUN servers from Twilio, falling back to public STUN only."""
    account_sid = _read_secret("TWILIO_ACCOUNT_SID")
    auth_token = _read_secret("TWILIO_AUTH_TOKEN")

    if not account_sid or not auth_token:
        logger.warning("Twilio credentials not set; using STUN only. WebRTC may fail behind strict NATs.")
        return FALLBACK_ICE_SERVERS

    try:
        from twilio.rest import Client

        token = Client(account_sid, auth_token).tokens.create()
        return token.ice_servers
    except Exception as e:
        logger.warning("Failed to fetch Twilio ICE servers (%s); using STUN only.", e)
        return FALLBACK_ICE_SERVERS
