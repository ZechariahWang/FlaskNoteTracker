function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

  function deleteStat() {
    const element = document.getElementById("stat");
    element.remove();
    console.log("Deleted")
  }