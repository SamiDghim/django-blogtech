import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["messages", "input"]

  connect() {
    console.log("Room controller connected!")
    this.scrollToBottom()
  }

  // Auto-scroll to bottom of messages
  scrollToBottom() {
    if (this.hasMessagesTarget) {
      this.messagesTarget.scrollTop = this.messagesTarget.scrollHeight
    }
  }

  // Handle message submission
  submitMessage(event) {
    event.preventDefault()
    
    const form = event.target
    const formData = new FormData(form)
    const messageInput = this.inputTarget
    const messageText = messageInput.value.trim()
    
    if (!messageText) return
    
    // Add message to UI immediately (optimistic update)
    this.addOptimisticMessage(messageText)
    
    // Clear input
    messageInput.value = ""
    
    // Submit form via Turbo
    fetch(form.action, {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'text/vnd.turbo-stream.html',
        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
      }
    })
    .then(response => response.text())
    .then(html => {
      // Handle Turbo Stream response
      if (html.includes('turbo-stream')) {
        document.body.insertAdjacentHTML('beforeend', html)
      }
    })
    .catch(error => {
      console.error('Error submitting message:', error)
      // Remove optimistic message on error
      this.removeOptimisticMessage()
    })
  }

  addOptimisticMessage(text) {
    const messageHtml = `
      <div class="thread optimistic-message" data-temporary="true">
        <div class="thread__top">
          <div class="thread__author">
            <span class="text-main font-medium">You</span>
            <small class="text-gray">just now</small>
          </div>
        </div>
        <div class="thread__details">
          <p class="text-light-gray">${text}</p>
        </div>
      </div>
    `
    
    if (this.hasMessagesTarget) {
      this.messagesTarget.insertAdjacentHTML('beforeend', messageHtml)
      this.scrollToBottom()
    }
  }

  removeOptimisticMessage() {
    const optimisticMessage = this.messagesTarget.querySelector('[data-temporary="true"]')
    if (optimisticMessage) {
      optimisticMessage.remove()
    }
  }

  // Handle real-time message updates (if WebSocket is added later)
  messageReceived(data) {
    const messageHtml = `
      <div class="thread">
        <div class="thread__top">
          <div class="thread__author">
            <span class="text-main font-medium">${data.username}</span>
            <small class="text-gray">${data.timestamp}</small>
          </div>
        </div>
        <div class="thread__details">
          <p class="text-light-gray">${data.message}</p>
        </div>
      </div>
    `
    
    if (this.hasMessagesTarget) {
      this.messagesTarget.insertAdjacentHTML('beforeend', messageHtml)
      this.scrollToBottom()
    }
  }
}
