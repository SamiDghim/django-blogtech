import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["menu"]
  static classes = ["show"]

  connect() {
    console.log("Dropdown controller connected!")
  }

  toggle() {
    if (this.menuTarget.classList.contains("show")) {
      this.close()
    } else {
      this.open()
    }
  }

  open() {
    this.menuTarget.classList.add("show")
    document.addEventListener("click", this.closeOnClickOutside.bind(this))
  }

  close() {
    this.menuTarget.classList.remove("show")
    document.removeEventListener("click", this.closeOnClickOutside.bind(this))
  }

  closeOnClickOutside(event) {
    if (!this.element.contains(event.target)) {
      this.close()
    }
  }

  disconnect() {
    document.removeEventListener("click", this.closeOnClickOutside.bind(this))
  }
}
