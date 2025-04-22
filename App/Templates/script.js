document.getElementById("quizForm").addEventListener("submit", function(e) {
    e.preventDefault();
  
    let score = 0;
    const form = e.target;
    for (let i = 1; i <= 5; i++) {
      score += parseInt(form["q" + i].value);
    }
  
    const result = document.getElementById("result");
    result.classList.remove("hidden");
  
    if (score <= 4) {
      result.textContent = "You seem to be doing well! Keep taking care of yourself.";
      result.style.color = "green";
    } else if (score <= 8) {
      result.textContent = "You might be experiencing mild mental stress. Consider healthy routines and talking to a friend.";
      result.style.color = "orange";
    } else {
      result.textContent = "You may be under significant mental strain. It might be helpful to talk to a professional.";
      result.style.color = "red";
    }
  });