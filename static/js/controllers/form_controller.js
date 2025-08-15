import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["submit"]

  connect() {
    console.log("Form controller connected!")
  }

  submit(event) {
    const submitButton = this.submitTarget
    
    // Disable submit button to prevent double submission
    submitButton.disabled = true
    submitButton.textContent = "Submitting..."
    
    // Re-enable after 3 seconds as fallback
    setTimeout(() => {
      submitButton.disabled = false
      submitButton.textContent = "Submit"
    }, 3000)
  }

  // Handle real-time form validation
  validate(event) {
    const input = event.target
    const value = input.value.trim()
    
    // Remove existing error classes
    input.classList.remove("border-red-500", "border-green-500")
    
    // Basic validation
    if (input.required && !value) {
      input.classList.add("border-red-500")
    } else if (value) {
      input.classList.add("border-green-500")
    }
  }

  // Auto-resize textarea
  autoResize(event) {
    const textarea = event.target
    textarea.style.height = "auto"
    textarea.style.height = textarea.scrollHeight + "px"
  }
}
