import qrcode

def generate_qr_code(upi_id: str, amount: int, origin: str, destination: str, date: str, ticket_id: str, filename: str):
    # Adding extra information to the payment_info URL
    payment_info = (
        f"upi://pay?pa={upi_id}&am={amount}&cu=INR"
        f"&origin={origin}&destination={destination}&date={date}&ticket_id={ticket_id}"
    )
    
    # Generate the QR code
    qr = qrcode.make(payment_info)
    qr.save(filename)
    
# Example usage
generate_qr_code(
    upi_id="vishal31apv@oksbi",
    amount=24,
    origin="Vadapalani",
    destination="Pachaiyappas College",
    date="14-10-2024 17:03",
    ticket_id="81242913",
    filename="custom_ticket_qr.png"
)
