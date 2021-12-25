const hambugerMenu = document.getElementById("hamburger");

hambugerMenu.addEventListener("click", () => {
  const categoryList = document.getElementById("category-list");
  categoryList.classList.toggle("show");
});
