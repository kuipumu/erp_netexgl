// Import resources.
import '../img/icons/android-chrome-192x192.png'
import '../img/icons/android-chrome-512x512.png'
import '../img/icons/apple-touch-icon.png'
import '../img/icons/browserconfig.xml'
import '../img/icons/favicon.ico'
import '../img/icons/favicon.svg'
import '../img/icons/favicon-16x16.png'
import '../img/icons/favicon-32x32.png'
import '../img/icons/mstile-70x70.png'
import '../img/icons/mstile-144x144.png'
import '../img/icons/mstile-150x150.png'
import '../img/icons/mstile-310x150.png'
import '../img/icons/mstile-310x310.png'
import '../img/icons/safari-pinned-tab.svg'
import '../img/icons/site.webmanifest'

window.autofillAddress = function(
    option, url, address_line1, address_line2, city_district,
    state_province, postal_code, country
){
    const selectField = document.querySelector(
        'select[name=' + option + ']'
    )
    const addressLine1Field = document.querySelector(
        'input[name=' + address_line1 +']'
    )
    const addressLine2Field = document.querySelector(
        'input[name=' + address_line2 + ']'
    )
    const cityDistrictField = document.querySelector(
        'input[name=' + city_district + ']'
    )
    const stateProvinceField = document.querySelector(
        'input[name=' + state_province + ']'
    )
    const postalCodeField = document.querySelector(
        'input[name=' + postal_code + ']'
    )
    const countryField = document.querySelector(
        'select[name=' + country + ']'
    )

    selectField.onchange=function() {
        const apiUrl = new URL(url)
        const params = {q: this.value}
        apiUrl.search = new URLSearchParams(params).toString();
        fetch(apiUrl)
            .then((response) => response.json())
            .then(function(data) {
                const fieldsToUpdate = [
                    {field:addressLine1Field,value:data.address_line1},
                    {field:addressLine2Field,value:data.address_line2},
                    {field:cityDistrictField,value:data.city_district},
                    {field:stateProvinceField,value:data.state_province},
                    {field:postalCodeField,value:data.postal_code},
                    {field:countryField,value:data.country},
                ]
                for (const { field,value } of fieldsToUpdate) {
                    if (!!field) {
                        field.value = ''
                        if (!!value) {
                            field.value = value
                        }
                        if (field == countryField) {
                            $('select[name=' + country + ']').trigger('change')
                        }
                    }
                }
            })
            .catch(function(error) {
                console.log(error);
            });
    }
}

// Hide field if the related checkbox is checked or not.
window.checkboxToggleField = function(option, field){
    const checkbox = document.querySelector(
        'input[name='+ option +']'
    )
    const inputField = document.querySelector(
        '.field-' + field
    )

    // Detect based on input.
    if (checkbox.checked == true) {
        inputField.style.display = 'block'
        inputField.removeAttribute('disabled')
    } else {
        inputField.style.display = 'none'
        inputField.setAttribute('disabled', true)
    }
    // Detect on input change
    checkbox.addEventListener('change', function () {
        if (checkbox.checked == true) {
            inputField.style.display = 'block'
            inputField.removeAttribute('disabled')
        } else {
            inputField.style.display = 'none'
            inputField.setAttribute('disabled', true)
        }
    })
}

