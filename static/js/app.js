// StudyBuddy JavaScript Entry Point
import "@hotwired/turbo"
import { Application } from "@hotwired/stimulus"

// Import Stimulus controllers
import HelloController from "./controllers/hello_controller.js"
import DropdownController from "./controllers/dropdown_controller.js"
import FormController from "./controllers/form_controller.js"
import RoomController from "./controllers/room_controller.js"

// Start Stimulus application
window.Stimulus = Application.start()

// Register controllers
Stimulus.register("hello", HelloController)
Stimulus.register("dropdown", DropdownController)
Stimulus.register("form", FormController)
Stimulus.register("room", RoomController)

// Configure Turbo
Turbo.session.drive = true

// Add loading indicator
document.addEventListener("turbo:before-visit", () => {
  document.body.classList.add("loading")
})

document.addEventListener("turbo:visit", () => {
  document.body.classList.remove("loading")
})

// Handle form submissions with Turbo
document.addEventListener("turbo:submit-start", () => {
  console.log("Form submission started")
})

document.addEventListener("turbo:submit-end", () => {
  console.log("Form submission completed")
})

// Show loading state
const style = document.createElement('style')
style.textContent = `
  .loading {
    cursor: wait;
  }
  .loading::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #71c6dd, #5dd693);
    z-index: 9999;
    animation: loading 1s infinite;
  }
  @keyframes loading {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }
`
document.head.appendChild(style)

console.log("StudyBuddy Turbo & Stimulus initialized! 🚀")
