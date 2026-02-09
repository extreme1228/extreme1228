const API_BASE = "/api/posts";

const createButton = document.querySelector("#create-post");
const saveButton = document.querySelector("#save-post");
const publishButton = document.querySelector("#publish-post");
const exportButton = document.querySelector("#export-posts");
const importInput = document.querySelector("#import-posts");

const titleInput = document.querySelector("#post-title");
const categoryInput = document.querySelector("#post-category");
const dateInput = document.querySelector("#post-date");
const urlInput = document.querySelector("#post-url");
const contentInput = document.querySelector("#post-content");

const postList = document.querySelector("#post-list");

const filters = document.querySelectorAll(".chip");

let posts = [];
let currentFilter = "all";
let editingId = null;

async function loadPosts() {
    const query = currentFilter === "all" ? "" : `?status=${currentFilter}`;
    const response = await fetch(`${API_BASE}${query}`);
    posts = await response.json();
}

function renderPosts() {
    postList.innerHTML = "";
    if (!posts.length) {
        const empty = document.createElement("div");
        empty.className = "card";
        empty.textContent = "No posts yet. Create your first draft.";
        postList.appendChild(empty);
        return;
    }

    posts.forEach(post => {
        const card = document.createElement("article");
        card.className = "card";

        const meta = document.createElement("p");
        meta.className = "blog-meta";
        meta.textContent = `${post.date || "No date"} · ${post.category} · ${post.status}`;

        const title = document.createElement("h3");
        title.textContent = post.title || "Untitled";

        const excerpt = document.createElement("p");
        excerpt.className = "muted";
        excerpt.textContent = post.content.slice(0, 140) + (post.content.length > 140 ? "..." : "");

        const actions = document.createElement("div");
        actions.className = "blog-actions";

        const editButton = document.createElement("button");
        editButton.className = "btn btn-ghost";
        editButton.textContent = "Edit";
        editButton.addEventListener("click", () => loadPost(post.id));

        const removeButton = document.createElement("button");
        removeButton.className = "btn btn-ghost";
        removeButton.textContent = "Delete";
        removeButton.addEventListener("click", () => deletePost(post.id));

        actions.append(editButton, removeButton);

        if (post.url) {
            const link = document.createElement("a");
            link.className = "text-link";
            link.href = post.url;
            link.target = "_blank";
            link.textContent = "External link";
            actions.appendChild(link);
        }

        card.append(meta, title, excerpt, actions);
        postList.appendChild(card);
    });
}

function resetForm() {
    titleInput.value = "";
    categoryInput.value = "notes";
    dateInput.value = "";
    urlInput.value = "";
    contentInput.value = "";
    editingId = null;
}

function getFormData() {
    return {
        title: titleInput.value.trim(),
        category: categoryInput.value,
        date: dateInput.value,
        url: urlInput.value.trim(),
        content: contentInput.value.trim()
    };
}

async function createPost(status) {
    const data = getFormData();
    if (!data.title || !data.content) {
        alert("Title and content are required.");
        return;
    }

    if (editingId) {
        await fetch(`${API_BASE}/${editingId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ...data, status })
        });
        editingId = null;
    } else {
        await fetch(API_BASE, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ...data, status })
        });
    }

    await loadPosts();
    renderPosts();
    resetForm();
}

async function loadPost(id) {
    const response = await fetch(`${API_BASE}/${id}`);
    if (!response.ok) return;
    const post = await response.json();

    titleInput.value = post.title;
    categoryInput.value = post.category;
    dateInput.value = post.date || "";
    urlInput.value = post.url || "";
    contentInput.value = post.content;
    editingId = post.id;
}

async function deletePost(id) {
    if (!confirm("Delete this post?")) return;
    await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
    await loadPosts();
    renderPosts();
}

async function exportPosts() {
    const response = await fetch(API_BASE);
    const data = await response.json();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "blog-posts.json";
    link.click();
    URL.revokeObjectURL(url);
}

async function importPosts(event) {
    const file = event.target.files[0];
    if (!file) return;

    const text = await file.text();
    try {
        const data = JSON.parse(text);
        if (!Array.isArray(data)) return;

        for (const post of data) {
            if (!post.title || !post.content) continue;
            await fetch(API_BASE, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    title: post.title,
                    category: post.category || "notes",
                    date: post.date || "",
                    url: post.url || "",
                    content: post.content,
                    status: post.status || "draft"
                })
            });
        }
        await loadPosts();
        renderPosts();
    } catch (error) {
        console.error("Invalid JSON", error);
    }
}

filters.forEach(filter => {
    filter.addEventListener("click", async () => {
        filters.forEach(item => item.classList.remove("is-active"));
        filter.classList.add("is-active");
        currentFilter = filter.dataset.filter;
        await loadPosts();
        renderPosts();
    });
});

createButton.addEventListener("click", () => resetForm());
saveButton.addEventListener("click", () => createPost("draft"));
publishButton.addEventListener("click", () => createPost("published"));
exportButton.addEventListener("click", exportPosts);
importInput.addEventListener("change", importPosts);

loadPosts().then(renderPosts);
