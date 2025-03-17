<script>
    let { data } = $props();
</script>



<h1>{data.item.title}</h1>
<div>{@html data.item.content}</div>
