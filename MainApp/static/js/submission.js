function KnowMore(){
    Swal.fire({
        title: 'Referral Code!!',
        html: `
            <p>Register with six teams from the same college and enjoy a reduced fee of ₹500 per team (instead of ₹600). <a class="know-more" href="../discount" >Read more</a> OR</p>
            <a class="know-more" href="../generateReferral/" target="_blank" class="swal2-referral-link">Generate a Referral Code Now</a>
            Or Enter the referral code if you already have one!!
        `,
        showCloseButton: true,
        customClass: {
            popup: 'swal2-fullscreen'
        },
        width: '100%',
        heightAuto: false,
        allowOutsideClick: false,
        allowEscapeKey: true
    });
}

async function Validateform() {
    const code = document.getElementById("referral_code").value;
    if (code.trim() === "") {
        // Allow form submission if referral code is empty
        return true;
    }

    setRequestHeader();
    const data = {
        'referral_code': code
    };

    try {
        await $.ajax({
            type: "POST",
            url: "/referralvalidation/",
            data: data
        });
        return true; // Return true if validation is successful
    } catch (error) {
        // Show an error message if validation fails
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Invalid Referral Code! Please try again.',
        });
        return false;
    }
}

async function ValidateAndSubmit(event) {
    event.preventDefault(); // Prevent form submission

    const isValid = await Validateform(); // Wait for referral code validation

    if (isValid) {
        event.target.submit(); // Submit form if validation passes
    }
}