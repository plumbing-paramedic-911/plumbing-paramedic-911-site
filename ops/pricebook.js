(function(root){
  async function loadAll(client){
    const items=[];
    const pageSize=500;
    for(let start=0;;start+=pageSize){
      const {data,error}=await client.from('price_book_items').select('*').eq('active',true).order('section_number').order('sku').range(start,start+pageSize-1);
      if(error)throw error;
      items.push(...(data||[]));
      if(!data||data.length<pageSize)return items;
    }
  }
  function filter(items,query,category){
    const text=query.trim().toLowerCase();
    return items.filter(x=>(!category||x.category===category)&&(!text||[x.sku,x.service_name,x.description,x.category].some(v=>String(v||'').toLowerCase().includes(text))));
  }
  const api={loadAll,filter};
  if(typeof module==='object'&&module.exports)module.exports=api;
  else root.PP911PriceBook=api;
})(typeof window==='object'?window:globalThis);
