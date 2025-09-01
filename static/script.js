document.addEventListener("DOMContentLoaded", () => {

  // Auto-hide flash messages
  const flashes = document.querySelectorAll(".flash li");
  flashes.forEach(flash => {
    setTimeout(() => {
      flash.style.transition = "opacity 0.5s ease";
      flash.style.opacity = 0;
      setTimeout(() => flash.remove(), 500);
    }, 4000);
  });

  // Confirm buddy request
  const requestForms = document.querySelectorAll(".send-request-form");
  requestForms.forEach(form => {
    form.addEventListener("submit", e => {
      const confirmSend = confirm("Do you want to send this buddy request?");
      if (!confirmSend) e.preventDefault();
    });
  });

  // Profile validation
  const profileForm = document.querySelector("form[action='/profile']");
  if (profileForm) {
    profileForm.addEventListener("submit", e => {
      const course = profileForm.querySelector("input[name='course']").value.trim();
      const skills = profileForm.querySelector("input[name='skills']").value.trim();
      const university = profileForm.querySelector("input[name='university']").value.trim();

      if (!course) {
        alert("Course is required!");
        e.preventDefault();
      } else if (course.length > 100 || skills.length > 255 || university.length > 100) {
        alert("Input too long! Please shorten your entries.");
        e.preventDefault();
      }
    });
  }

  // Highlight match card
  const matchItems = document.querySelectorAll(".match-item");
  matchItems.forEach(item => {
    item.addEventListener("mouseenter", () => {
      item.style.backgroundColor = "#f0f8ff";
      item.style.transition = "background-color 0.3s ease";
    });
    item.addEventListener("mouseleave", () => {
      item.style.backgroundColor = "transparent";
    });
  });

  // Skill filter
  const skillFilter = document.querySelector("#skill-filter");
  if (skillFilter) {
    skillFilter.addEventListener("input", () => {
      const filterText = skillFilter.value.toLowerCase();
      matchItems.forEach(item => {
        const skills = item.dataset.skills.toLowerCase();
        item.style.display = skills.includes(filterText) ? "" : "none";
      });
    });
  }

  // Chat scroll to bottom
  const chatBox = document.getElementById("chat-box");
  if(chatBox) { chatBox.scrollTop = chatBox.scrollHeight; }

});
