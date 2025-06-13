class InvoiceExceptions(Exception):
    """Custom exception for errors during invoice processing."""
    def __init__(self, message="An error occurred while processing invoices."):
        super().__init__(message)
    
