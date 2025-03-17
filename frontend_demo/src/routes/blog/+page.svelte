<script>
    let { data } = $props();
</script>

<h1>blog</h1>

<ul>
    <li><a href="/blog/one">one</a></li>
    <li><a href="/blog/two">two</a></li>
    <li><a href="/blog/one">three</a></li>
</ul>

{#each data.summaires as {slug,title} }
    <li>
        <a href="/blog/{slug}">{title}</a>
    </li>
{/each}
