import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["name"]

  connect() {
    console.log("Hello controller connected!", this.element)
  }

  greet() {
    const name = this.nameTarget.value
    alert(`Hello, ${name}!`)
  }
}
