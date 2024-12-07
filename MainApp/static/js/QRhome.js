document.addEventListener("DOMContentLoaded", () => {
    const qrReader = new Html5Qrcode("qr-reader");
  
    let scanningPaused = false; // State to control scanning pause/resume
    const config = {
      fps: 10, // Frames per second for scanning
      qrbox: { width: 250, height: 250 }, // Scanner box size
    };
  
    const onScanSuccess = (decodedText) => {
      if (scanningPaused) {
        return; // Ignore scans if paused
      }
  
      scanningPaused = true; // Pause scanning
      console.log("Scanned QR Code:", decodedText);
  
      // Send the scanned data to the server
      fetch("", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ unique_code: decodedText }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            Swal.fire("Success", data.success, "success")
              .then(() => {
                // Show confirmation dialog
                Swal.fire({
                  title: "Ready to continue?",
                  text: "You can now proceed with scanning.",
                  icon: data.success.includes("marked as completed") ? "success" : "info",
                  confirmButtonText: "OK",
                }).then(() => {
                  scanningPaused = false; // Resume scanning
                });
              });
          } else if (data.error) {
            Swal.fire("Error", data.error, "error")
              .then(() => {
                // Show confirmation dialog
                Swal.fire({
                  title: "Ready to continue?",
                  text: "You can now proceed with scanning.",
                  icon: "error",
                  confirmButtonText: "OK",
                }).then(() => {
                  scanningPaused = false; // Resume scanning
                });
              });
          }
        })
        .catch((error) => {
          Swal.fire("Error", "Something went wrong while sending the QR code data.", "error")
            .then(() => {
              // Show confirmation dialog
              Swal.fire({
                title: "Ready to continue?",
                text: "You can now proceed with scanning.",
                icon: "warning",
                confirmButtonText: "OK",
              }).then(() => {
                scanningPaused = false; // Resume scanning
              });
            });
          console.error("Fetch error:", error);
        });
    };
  
    // Start the QR reader
    qrReader.start(
      { facingMode: "environment" }, // Use the back camera
      config,
      onScanSuccess
    ).catch((err) => {
      console.error("QR Code Scanner error:", err);
      Swal.fire("Error", "Could not start the QR scanner. Please check your camera settings.", "error");
    });
  });
  