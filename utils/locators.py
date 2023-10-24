from typing import Dict, List, Tuple, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

login_elements: Dict[
    str,
    Tuple[Union[EC.visibility_of_element_located, EC.element_to_be_clickable], By, str],
] = {
    "email": (EC.visibility_of_element_located, By.ID, "email"),
    "password": (EC.visibility_of_element_located, By.ID, "password"),
    "login_button": (
        EC.element_to_be_clickable,
        By.CSS_SELECTOR,
        "button.btn.btn-primary",
    ),
}

alert_box_message: Dict[
    str, Tuple[Union[EC.visibility_of_element_located, By, str]]
] = {
    "alert_box": (
        EC.visibility_of_element_located,
        By.CLASS_NAME,
        "alert-message",
    )
}

ALERT_MESSAGES: List[str] = [
    "The username or password did not match. Please try again.",
    "El nombre de usuario o la contraseña no coinciden. Vuelve a intentarlo.",
]


oauth_elements: Dict[str, Tuple[Union[EC.element_to_be_clickable, By, str]]] = {
    "authorize_button": (
        EC.element_to_be_clickable,
        By.CSS_SELECTOR,
        "button#authorize",
    )
}

correct_elevation_elements: Dict[
    str,
    Tuple[Union[EC.visibility_of_element_located, EC.element_to_be_clickable], By, str],
] = {
    "indoor_cyclig": (
        EC.visibility_of_element_located,
        By.CSS_SELECTOR,
        "h2.text-title3.text-book.marginless",
    ),
    "title_header": (EC.visibility_of_element_located, By.CLASS_NAME, "title"),
    "options_button": (
        EC.element_to_be_clickable,
        By.CSS_SELECTOR,
        "div.app-icon.icon-nav-more",
    ),
    "revert_button": (
        EC.presence_of_element_located,
        By.CSS_SELECTOR,
        "div[data-react-class='CorrectElevation']",
    ),
    "correct_button": (
        EC.element_to_be_clickable,
        By.CSS_SELECTOR,
        "div[data-react-class='CorrectElevation']",
    ),
    "click_correct_button": (
        EC.element_to_be_clickable,
        By.CSS_SELECTOR,
        "button.Button--primary--cUgAV[type='submit']",
    ),
}
