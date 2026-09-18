
/* ── 九宮飛星（蘇民峰原作化解物品）── */
const STAR_DATA={
  1:{name:'一白貪狼',el:'水',type:'auspicious',label:'桃花位',remedy:'宜放音樂盒及一杯水，催旺桃花人緣',fortune:'桃花人緣暢旺之年，感情、人際皆宜把握，單身者機會明顯。'},
  2:{name:'二黑巨門',el:'土',type:'danger',label:'細病位',remedy:'宜放音樂盒，化病消災',fortune:'病符當令，留意腸胃及婦女健康，此方宜靜不宜動。'},
  3:{name:'三碧祿存',el:'木',type:'inauspicious',label:'爭鬥位',remedy:'宜放粉紅色物件，化解是非',fortune:'是非口舌之年，忌衝動爭拗，以靜制動、慎言為上。'},
  4:{name:'四綠文曲',el:'木',type:'auspicious',label:'文昌位',remedy:'宜放四枝富貴竹或一杯水，催旺文昌',fortune:'文昌當旺，利進修考試、文書簽約，思路清晰易有成。'},
  5:{name:'五黃廉貞',el:'土',type:'danger',label:'大病位',remedy:'宜放音樂盒及一杯水，化五黃煞',fortune:'災病潛伏，此方大忌動土裝修，化煞為先、低調為上。'},
  6:{name:'六白武曲',el:'金',type:'auspicious',label:'武曲位',remedy:'宜放一杯水催財或八粒白石利升遷',fortune:'偏財與權貴之助，利升遷求職、地位提升，把握良機。'},
  7:{name:'七赤破軍',el:'金',type:'inauspicious',label:'破軍位',remedy:'宜放一杯水，洩化破軍之氣',fortune:'破財之星，防被騙失竊，理財宜保守，不宜投機。'},
  8:{name:'八白左輔',el:'土',type:'auspicious',label:'財位',remedy:'宜放一杯水，催旺財星',fortune:'當時得令之財星，大利置業儲蓄投資，財運全年最旺。'},
  9:{name:'九紫右弼',el:'火',type:'auspicious',label:'喜慶位',remedy:'宜放四盆植物及九枝紅花，催旺喜慶',fortune:'喜慶桃花之星，利婚嫁添丁、喜事臨門，人緣旺盛。'}
};
const LUOSHU=[[4,9,2],[3,5,7],[8,1,6]];
const COMPASS=[['東南 (SE)','南 (S)','西南 (SW)'],['東 (E)','中宮','西 (W)'],['東北 (NE)','北 (N)','西北 (NW)']];
const DIRS_CN=['東南','南','西南','東','中宮','西','東北','北','西北'];
function centerStar(y){let c=3-((y-2024)%9);if(c<=0)c+=9;return c}
function getGrid(c){return LUOSHU.map(r=>r.map(v=>(((v+c-6)%9+9)%9)+1))}
/* 九宮格渲染共用（renderFly / renderDoor 用同一套 cell 結構） */
function fillGrid(gridEl,g,labels,centerRC,withRemedy){
  gridEl.innerHTML='';
  g.forEach((row,ri)=>row.forEach((s,ci)=>{
    const d=STAR_DATA[s];
    const cell=document.createElement('div');
    const isCenter=centerRC&&centerRC[0]===ri&&centerRC[1]===ci;
    cell.className='fly-cell '+d.type+(isCenter?' center':'');
    cell.innerHTML='<div class="fly-compass">'+labels[ri*3+ci]+'</div><div class="star-num">'+s+'</div><div class="star-info">'+d.name+' ('+d.el+') · '+d.label+'</div>'+(withRemedy?'<div class="star-remedy">'+d.remedy+'</div>':'');
    gridEl.appendChild(cell);
  }));
}
function renderFly(){
  const y=+document.getElementById('fly-year').value;
  const c=centerStar(y),g=getGrid(c);
  fillGrid(document.getElementById('fly-grid'),g,COMPASS.flat(),null,true);
  document.getElementById('fly-label').textContent=y+'年九宮飛星（'+STAR_DATA[c].name+'入中）';
  document.getElementById('fly-dir').textContent='上南（離）下北（坎）· 左東右西 · 洛書戴九履一';
}

/* ── 犯太歲（蘇民峰規則：佩戴太歲生肖三合/六合飾物，排除自身犯太歲者）── */
const ANIMALS=['鼠','牛','虎','兔','龍','蛇','馬','羊','猴','雞','狗','豬'];
const BRANCHES=['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
const A2B={};ANIMALS.forEach((a,i)=>{A2B[a]=BRANCHES[i]});
const LIUHE={鼠:'牛',牛:'鼠',虎:'豬',兔:'狗',龍:'雞',蛇:'猴',馬:'羊',羊:'馬',猴:'蛇',雞:'龍',狗:'兔',豬:'虎'};
const SANHE={鼠:['猴','龍'],牛:['蛇','雞'],虎:['馬','狗'],兔:['豬','羊'],龍:['猴','鼠'],蛇:['雞','牛'],馬:['虎','狗'],羊:['兔','豬'],猴:['龍','鼠'],雞:['蛇','牛'],狗:['虎','馬'],豬:['兔','羊']};
const TAISUI={
  2024:{b:'辰',z:'龍',clash:'狗',punish:'龍（自刑）',harm:'兔',dest:'牛'},
  2025:{b:'巳',z:'蛇',clash:'豬',punish:'猴',harm:'虎',dest:'猴'},
  2026:{b:'午',z:'馬',clash:'鼠',punish:'馬（自刑）',harm:'牛',dest:'兔'},
  2027:{b:'未',z:'羊',clash:'牛',punish:'狗',harm:'鼠',dest:'狗'},
  2028:{b:'申',z:'猴',clash:'虎',punish:'蛇',harm:'豬',dest:'蛇'},
  2029:{b:'酉',z:'雞',clash:'兔',punish:'雞（自刑）',harm:'狗',dest:'鼠'},
  2030:{b:'戌',z:'狗',clash:'龍',punish:'牛',harm:'雞',dest:'羊'}
};
function getTSZodiacs(ts){
  const s=new Set();s.add(ts.z);s.add(ts.clash);
  ts.punish.split('、').forEach(p=>s.add(p.replace('（自刑）','')));
  s.add(ts.harm);s.add(ts.dest);return s;
}
function renderTS(){
  const y=+document.getElementById('ts-year').value;
  const z=document.getElementById('ts-zodiac').value;
  const ts=TAISUI[y];if(!ts)return;
  const r=document.getElementById('ts-result');r.style.display='block';
  let type,label,detail;
  if(z===ts.z){type='值太歲';label='值';detail=y+'年歲次'+ts.b+'，屬'+z+'為值太歲（本命年），運程起伏較大。'}
  else if(z===ts.clash){type='沖太歲';label='沖';detail='屬'+z+'與太歲'+ts.z+'相沖（'+A2B[z]+'沖'+ts.b+'），主動求變則吉，被動應變則滯。'}
  else if(ts.punish.includes(z)){type='刑太歲';label='刑';detail='屬'+z+'遭遇刑太歲，易惹官非口舌，宜守不宜攻。'}
  else if(z===ts.harm){type='害太歲';label='害';detail='屬'+z+'與太歲'+ts.z+'相害，防小人暗害，注意健康。'}
  else if(z===ts.dest){type='破太歲';label='破';detail='屬'+z+'與太歲'+ts.z+'相破，慎防破財，保守理財。'}
  else{type='無犯太歲';label='-';detail='屬'+z+'今年無犯太歲，運程相對平穩，宜把握機遇。'}
  const cls=label==='-'?'normal':'tai';
  const tsZods=getTSZodiacs(ts);
  // 蘇：佩戴當年太歲生肖的三合/六合飾物（合太歲）；若該三合/六合生肖本身亦犯太歲則不可佩戴
  const taishou=ts.z;
  const partners=[LIUHE[taishou],...SANHE[taishou]];
  const forbidden=[];
  const safe=[];
  partners.forEach(p=>{if(tsZods.has(p))forbidden.push(p+'（'+p+'今年犯太歲，不宜佩戴）');else safe.push(p)});
  let pendantLine='<b>飾物建議：</b>';
  if(safe.length){pendantLine+='屬'+z+'可佩戴 <span style="color:var(--green);font-weight:600">'+safe.join('、')+'</span> 生肖飾物——與太歲'+taishou+'三合/六合，可和合太歲、催旺人緣。';}
  if(forbidden.length){pendantLine+='<br><span style="color:var(--orange);font-size:12.5px">⚠️ '+forbidden.join('；')+'</span>';}
  r.innerHTML='<div class="ts-rel"><span class="badge '+cls+'">'+type+'</span> '+detail+'</div>'
    +'<div class="ts-remedy"><b>化解建議：</b>'+(label!=='-'?'拜太歲、穿紅內衣或紅繩、避免探病問喪':'保持心態平和，多行善事。')+'</div>'
    +'<div class="ts-remedy">'+pendantLine+'</div>';
}


/* ── 寒熱平命計算器（蘇：熱=立夏~立秋；平=立春~立夏+立秋~立冬；寒=立冬~立春）── */
const MING={"1930":{"驚蟄":"1930-03-06","清明":"1930-04-06","立夏":"1930-05-06","立秋":"1930-08-08"},"1931":{"驚蟄":"1931-03-07","清明":"1931-04-06","立夏":"1931-05-07","立秋":"1931-08-09"},"1932":{"驚蟄":"1932-03-06","清明":"1932-04-05","立夏":"1932-05-06","立秋":"1932-08-08"},"1933":{"驚蟄":"1933-03-06","清明":"1933-04-05","立夏":"1933-05-06","立秋":"1933-08-08"},"1934":{"驚蟄":"1934-03-06","清明":"1934-04-05","立夏":"1934-05-06","立秋":"1934-08-08"},"1935":{"驚蟄":"1935-03-07","清明":"1935-04-06","立夏":"1935-05-06","立秋":"1935-08-08"},"1936":{"驚蟄":"1936-03-06","清明":"1936-04-05","立夏":"1936-05-06","立秋":"1936-08-08"},"1937":{"驚蟄":"1937-03-06","清明":"1937-04-05","立夏":"1937-05-06","立秋":"1937-08-08"},"1938":{"驚蟄":"1938-03-06","清明":"1938-04-05","立夏":"1938-05-06","立秋":"1938-08-08"},"1939":{"驚蟄":"1939-03-06","清明":"1939-04-06","立夏":"1939-05-06","立秋":"1939-08-08"},"1940":{"驚蟄":"1940-03-06","清明":"1940-04-05","立夏":"1940-05-06","立秋":"1940-08-08"},"1941":{"驚蟄":"1941-03-06","清明":"1941-04-05","立夏":"1941-05-06","立秋":"1941-08-08"},"1942":{"驚蟄":"1942-03-06","清明":"1942-04-05","立夏":"1942-05-06","立秋":"1942-08-08"},"1943":{"驚蟄":"1943-03-06","清明":"1943-04-06","立夏":"1943-05-06","立秋":"1943-08-08"},"1944":{"驚蟄":"1944-03-06","清明":"1944-04-05","立夏":"1944-05-06","立秋":"1944-08-08"},"1945":{"驚蟄":"1945-03-06","清明":"1945-04-05","立夏":"1945-05-06","立秋":"1945-08-08"},"1946":{"驚蟄":"1946-03-06","清明":"1946-04-05","立夏":"1946-05-06","立秋":"1946-08-08"},"1947":{"驚蟄":"1947-03-06","清明":"1947-04-06","立夏":"1947-05-06","立秋":"1947-08-08"},"1948":{"驚蟄":"1948-03-06","清明":"1948-04-05","立夏":"1948-05-06","立秋":"1948-08-08"},"1949":{"驚蟄":"1949-03-06","清明":"1949-04-05","立夏":"1949-05-06","立秋":"1949-08-08"},"1950":{"驚蟄":"1950-03-06","清明":"1950-04-05","立夏":"1950-05-06","立秋":"1950-08-08"},"1951":{"驚蟄":"1951-03-06","清明":"1951-04-06","立夏":"1951-05-06","立秋":"1951-08-08"},"1952":{"驚蟄":"1952-03-06","清明":"1952-04-05","立夏":"1952-05-06","立秋":"1952-08-08"},"1953":{"驚蟄":"1953-03-06","清明":"1953-04-05","立夏":"1953-05-06","立秋":"1953-08-08"},"1954":{"驚蟄":"1954-03-06","清明":"1954-04-05","立夏":"1954-05-06","立秋":"1954-08-08"},"1955":{"驚蟄":"1955-03-06","清明":"1955-04-06","立夏":"1955-05-06","立秋":"1955-08-08"},"1956":{"驚蟄":"1956-03-06","清明":"1956-04-05","立夏":"1956-05-06","立秋":"1956-08-08"},"1957":{"驚蟄":"1957-03-06","清明":"1957-04-05","立夏":"1957-05-06","立秋":"1957-08-08"},"1958":{"驚蟄":"1958-03-06","清明":"1958-04-05","立夏":"1958-05-06","立秋":"1958-08-08"},"1959":{"驚蟄":"1959-03-06","清明":"1959-04-06","立夏":"1959-05-06","立秋":"1959-08-08"},"1960":{"驚蟄":"1960-03-06","清明":"1960-04-05","立夏":"1960-05-06","立秋":"1960-08-08"},"1961":{"驚蟄":"1961-03-06","清明":"1961-04-05","立夏":"1961-05-06","立秋":"1961-08-08"},"1962":{"驚蟄":"1962-03-06","清明":"1962-04-05","立夏":"1962-05-06","立秋":"1962-08-08"},"1963":{"驚蟄":"1963-03-06","清明":"1963-04-06","立夏":"1963-05-06","立秋":"1963-08-08"},"1964":{"驚蟄":"1964-03-06","清明":"1964-04-05","立夏":"1964-05-05","立秋":"1964-08-08"},"1965":{"驚蟄":"1965-03-06","清明":"1965-04-05","立夏":"1965-05-06","立秋":"1965-08-08"},"1966":{"驚蟄":"1966-03-06","清明":"1966-04-05","立夏":"1966-05-06","立秋":"1966-08-08"},"1967":{"驚蟄":"1967-03-06","清明":"1967-04-05","立夏":"1967-05-06","立秋":"1967-08-08"},"1968":{"驚蟄":"1968-03-06","清明":"1968-04-05","立夏":"1968-05-05","立秋":"1968-08-07"},"1969":{"驚蟄":"1969-03-06","清明":"1969-04-05","立夏":"1969-05-06","立秋":"1969-08-08"},"1970":{"驚蟄":"1970-03-06","清明":"1970-04-05","立夏":"1970-05-06","立秋":"1970-08-08"},"1971":{"驚蟄":"1971-03-06","清明":"1971-04-05","立夏":"1971-05-06","立秋":"1971-08-08"},"1972":{"驚蟄":"1972-03-05","清明":"1972-04-05","立夏":"1972-05-05","立秋":"1972-08-07"},"1973":{"驚蟄":"1973-03-06","清明":"1973-04-05","立夏":"1973-05-06","立秋":"1973-08-08"},"1974":{"驚蟄":"1974-03-06","清明":"1974-04-05","立夏":"1974-05-06","立秋":"1974-08-08"},"1975":{"驚蟄":"1975-03-06","清明":"1975-04-05","立夏":"1975-05-06","立秋":"1975-08-08"},"1976":{"驚蟄":"1976-03-05","清明":"1976-04-05","立夏":"1976-05-05","立秋":"1976-08-07"},"1977":{"驚蟄":"1977-03-06","清明":"1977-04-05","立夏":"1977-05-06","立秋":"1977-08-08"},"1978":{"驚蟄":"1978-03-06","清明":"1978-04-05","立夏":"1978-05-06","立秋":"1978-08-08"},"1979":{"驚蟄":"1979-03-06","清明":"1979-04-05","立夏":"1979-05-06","立秋":"1979-08-08"},"1980":{"驚蟄":"1980-03-05","清明":"1980-04-05","立夏":"1980-05-05","立秋":"1980-08-07"},"1981":{"驚蟄":"1981-03-06","清明":"1981-04-05","立夏":"1981-05-06","立秋":"1981-08-08"},"1982":{"驚蟄":"1982-03-06","清明":"1982-04-05","立夏":"1982-05-06","立秋":"1982-08-08"},"1983":{"驚蟄":"1983-03-06","清明":"1983-04-05","立夏":"1983-05-06","立秋":"1983-08-08"},"1984":{"驚蟄":"1984-03-05","清明":"1984-04-05","立夏":"1984-05-05","立秋":"1984-08-07"},"1985":{"驚蟄":"1985-03-06","清明":"1985-04-05","立夏":"1985-05-06","立秋":"1985-08-08"},"1986":{"驚蟄":"1986-03-06","清明":"1986-04-05","立夏":"1986-05-06","立秋":"1986-08-08"},"1987":{"驚蟄":"1987-03-06","清明":"1987-04-05","立夏":"1987-05-06","立秋":"1987-08-08"},"1988":{"驚蟄":"1988-03-05","清明":"1988-04-05","立夏":"1988-05-05","立秋":"1988-08-07"},"1989":{"驚蟄":"1989-03-06","清明":"1989-04-05","立夏":"1989-05-06","立秋":"1989-08-08"},"1990":{"驚蟄":"1990-03-06","清明":"1990-04-05","立夏":"1990-05-06","立秋":"1990-08-08"},"1991":{"驚蟄":"1991-03-06","清明":"1991-04-05","立夏":"1991-05-06","立秋":"1991-08-08"},"1992":{"驚蟄":"1992-03-05","清明":"1992-04-05","立夏":"1992-05-05","立秋":"1992-08-07"},"1993":{"驚蟄":"1993-03-06","清明":"1993-04-05","立夏":"1993-05-06","立秋":"1993-08-08"},"1994":{"驚蟄":"1994-03-06","清明":"1994-04-05","立夏":"1994-05-06","立秋":"1994-08-08"},"1995":{"驚蟄":"1995-03-06","清明":"1995-04-05","立夏":"1995-05-06","立秋":"1995-08-08"},"1996":{"驚蟄":"1996-03-05","清明":"1996-04-05","立夏":"1996-05-05","立秋":"1996-08-07"},"1997":{"驚蟄":"1997-03-06","清明":"1997-04-05","立夏":"1997-05-05","立秋":"1997-08-07"},"1998":{"驚蟄":"1998-03-06","清明":"1998-04-05","立夏":"1998-05-06","立秋":"1998-08-08"},"1999":{"驚蟄":"1999-03-06","清明":"1999-04-05","立夏":"1999-05-06","立秋":"1999-08-08"},"2000":{"驚蟄":"2000-03-05","清明":"2000-04-04","立夏":"2000-05-05","立秋":"2000-08-07"},"2001":{"驚蟄":"2001-03-06","清明":"2001-04-05","立夏":"2001-05-05","立秋":"2001-08-07"},"2002":{"驚蟄":"2002-03-06","清明":"2002-04-05","立夏":"2002-05-06","立秋":"2002-08-08"},"2003":{"驚蟄":"2003-03-06","清明":"2003-04-05","立夏":"2003-05-06","立秋":"2003-08-08"},"2004":{"驚蟄":"2004-03-05","清明":"2004-04-04","立夏":"2004-05-05","立秋":"2004-08-07"},"2005":{"驚蟄":"2005-03-05","清明":"2005-04-05","立夏":"2005-05-05","立秋":"2005-08-07"},"2006":{"驚蟄":"2006-03-06","清明":"2006-04-05","立夏":"2006-05-06","立秋":"2006-08-08"},"2007":{"驚蟄":"2007-03-06","清明":"2007-04-05","立夏":"2007-05-06","立秋":"2007-08-08"},"2008":{"驚蟄":"2008-03-05","清明":"2008-04-04","立夏":"2008-05-05","立秋":"2008-08-07"},"2009":{"驚蟄":"2009-03-05","清明":"2009-04-05","立夏":"2009-05-05","立秋":"2009-08-07"},"2010":{"驚蟄":"2010-03-06","清明":"2010-04-05","立夏":"2010-05-06","立秋":"2010-08-08"},"2011":{"驚蟄":"2011-03-06","清明":"2011-04-05","立夏":"2011-05-06","立秋":"2011-08-08"},"2012":{"驚蟄":"2012-03-05","清明":"2012-04-04","立夏":"2012-05-05","立秋":"2012-08-07"},"2013":{"驚蟄":"2013-03-05","清明":"2013-04-05","立夏":"2013-05-05","立秋":"2013-08-07"},"2014":{"驚蟄":"2014-03-06","清明":"2014-04-05","立夏":"2014-05-06","立秋":"2014-08-08"},"2015":{"驚蟄":"2015-03-06","清明":"2015-04-05","立夏":"2015-05-06","立秋":"2015-08-08"},"2016":{"驚蟄":"2016-03-05","清明":"2016-04-04","立夏":"2016-05-05","立秋":"2016-08-07"},"2017":{"驚蟄":"2017-03-05","清明":"2017-04-05","立夏":"2017-05-05","立秋":"2017-08-07"},"2018":{"驚蟄":"2018-03-06","清明":"2018-04-05","立夏":"2018-05-06","立秋":"2018-08-08"},"2019":{"驚蟄":"2019-03-06","清明":"2019-04-05","立夏":"2019-05-06","立秋":"2019-08-08"},"2020":{"驚蟄":"2020-03-05","清明":"2020-04-04","立夏":"2020-05-05","立秋":"2020-08-07"},"2021":{"驚蟄":"2021-03-05","清明":"2021-04-05","立夏":"2021-05-05","立秋":"2021-08-07"},"2022":{"驚蟄":"2022-03-06","清明":"2022-04-05","立夏":"2022-05-06","立秋":"2022-08-08"},"2023":{"驚蟄":"2023-03-06","清明":"2023-04-05","立夏":"2023-05-06","立秋":"2023-08-08"},"2024":{"驚蟄":"2024-03-05","清明":"2024-04-04","立夏":"2024-05-05","立秋":"2024-08-07"},"2025":{"驚蟄":"2025-03-05","清明":"2025-04-05","立夏":"2025-05-05","立秋":"2025-08-07"},"2026":{"驚蟄":"2026-03-06","清明":"2026-04-05","立夏":"2026-05-05","立秋":"2026-08-07"},"2027":{"驚蟄":"2027-03-06","清明":"2027-04-05","立夏":"2027-05-06","立秋":"2027-08-08"},"2028":{"驚蟄":"2028-03-05","清明":"2028-04-04","立夏":"2028-05-05","立秋":"2028-08-07"},"2029":{"驚蟄":"2029-03-05","清明":"2029-04-04","立夏":"2029-05-05","立秋":"2029-08-07"},"2030":{"驚蟄":"2030-03-06","清明":"2030-04-05","立夏":"2030-05-05","立秋":"2030-08-07"},"2031":{"驚蟄":"2031-03-06","清明":"2031-04-05","立夏":"2031-05-06","立秋":"2031-08-08"},"2032":{"驚蟄":"2032-03-05","清明":"2032-04-04","立夏":"2032-05-05","立秋":"2032-08-07"},"2033":{"驚蟄":"2033-03-05","清明":"2033-04-04","立夏":"2033-05-05","立秋":"2033-08-07"},"2034":{"驚蟄":"2034-03-06","清明":"2034-04-05","立夏":"2034-05-05","立秋":"2034-08-07"},"2035":{"驚蟄":"2035-03-06","清明":"2035-04-05","立夏":"2035-05-06","立秋":"2035-08-08"}};
function calcMing(){
  const v=document.getElementById('ming-date').value;
  if(!v){return;}
  const [y,m,d]=v.split('-').map(Number);
  const t=MING[y];
  if(!t){document.getElementById('ming-result').innerHTML='<p style="color:var(--red)">年份超出範圍（1930-2035）</p>';document.getElementById('ming-result').style.display='block';return;}
  let ming_='',seas='';
  // 蘇民峰官方定義（masterso.com 原文）：
  // 寒命 = 立秋(8/8)後 ~ 驚蟄(3/6)前（跨年）；熱命 = 立夏(5/6)後 ~ 立秋前；平命 = 驚蟄後 ~ 立夏前（清明前較平，清明後較熱之平命）
  if(v>=t['立秋']||v<t['驚蟄']){ming_='寒命人';seas='立秋後（8/8）至翌年驚蟄前（3/6）出生——全年最長時段（秋、冬、早春）';}
  else if(v>=t['立夏']&&v<t['立秋']){ming_='熱命人';seas='立夏後（5/6）至立秋前（8/8）出生（夏天）';}
  else if(v>=t['清明']){ming_='平命人';seas='清明後（4/5）至立夏前（5/6）出生——較熱之平命';}
  else{ming_='平命人';seas='驚蟄後（3/6）至清明前（4/5）出生——較平命';}
  // 定理：寒命喜火（木生火）、熱命喜水（金生水）、平命喜水不忌火，以水運較佳（土為平：帶水濕土、帶火乾土）
  const detail={
    '寒命人':['喜用：火（木生火助火勢）','喜向東南、南方；利青綠紅橙紫','2027 丁未火土燥熱之年 — 對寒命人特別有利，把握2022-2027木火運尾聲，積極進取。','寒命人一生以火運、木火流年為佳，水運則易見停滯。'],
    '熱命人':['喜用：水（金生水助水勢）','喜向西北、北方；利白金銀黑灰藍','2027 火土之年偏燥 — 對熱命人不利，宜守靜，待2028秋後金水運起再進攻。','熱命人一生以水運、金水流年為佳，火土流年則宜收歛。'],
    '平命人':['喜用：水（水火不忌，然以水運較佳）','五行皆可為用，土最中性','2027 丁未火土之年 — 中規中矩，無大起亦無大落，穩中求進即可。','平命人喜水不忌火，濕土為佳，乾土稍遜，故大水年固好，小水年亦利。']
  }[ming_];
  const season=[['寒命人','var(--teal)'],['熱命人','var(--orange)'],['平命人','var(--accent)']].find(x=>x[0]===ming_);
  document.getElementById('ming-result').innerHTML=
    '<div class="info-item" style="margin-bottom:10px"><div class="k">你係</div><div class="v" style="font-size:22px;font-weight:700;color:'+season[1]+'">'+ming_+'</div><div class="k" style="margin-top:6px">'+seas+'</div></div>'+
    '<div class="info-grid">'+detail.map(x=>'<div class="info-item"><div class="v">'+x+'</div></div>').join('')+'</div>'+
    '<p style="font-size:11.5px;color:var(--dim);margin-top:10px">※ 依據蘇民峰官方定義（masterso.com 玄學教室·風水命理析疑）：立秋後至驚蟄前為寒命、立夏後至立秋前為熱命、驚蟄後至立夏前為平命（清明前較平／清明後較熱之平命）。</p>';
  document.getElementById('ming-result').style.display='block';
}

/* ── 大門地氈（蘇民峰旺宅化病法：每年飛星方位→地氈色/化解物，通用推理體系）── */
/* 星名/屬性/稱呼由 STAR_DATA 提供，這裡只保留地氈處理（避免重複資料） */
const DOOR_REQUIRE = {
  1:{treat:'催桃花：門外放粉紅色地氈；已婚防桃花劫：門內放灰色或藍色地氈洩之'},
  2:{treat:'門內放灰色地氈，地氈底放金屬物件（金泄土），化病星'},
  3:{treat:'門內外放粉紅色地氈（火泄木），化解是非'},
  4:{treat:'門內放灰色地氈，並在門內外放綠色布或一杯水，催旺文昌'},
  5:{treat:'門內灰色地氈＋屋內金屬物件＋掛風鈴＋門旁音樂盒（金泄土），化五黃煞'},
  6:{treat:'門外放黃或啡色地氈（土生金）＋門內灰色地氈，利武職財運升遷'},
  7:{treat:'門內放灰色地氈引財（金生水），或門旁放一杯水洩金煞'},
  8:{treat:'門外放紅色地氈（火生土），催旺財星'},
  9:{treat:'室外放綠色地氈（木生火），催旺喜慶桃花'}
};
function renderDoor(){
  const y=+document.getElementById('door-year').value;
  const c=centerStar(y),g=getGrid(c);
  const d=document.getElementById('door-dir').value;
  const pos={東南:[0,0],南:[0,1],西南:[0,2],東:[1,0],中宮:[1,1],西:[1,2],東北:[2,0],北:[2,1],西北:[2,2]}[d];
  if(!pos)return;
  const star=g[pos[0]][pos[1]];
  const info=STAR_DATA[star];
  const r=DOOR_REQUIRE[star];
  const el=document.getElementById('door-result');
  el.style.display='block';
  const ausp=star===8||star===9||star===4||star===6||star===1;
  el.innerHTML='<div class="ts-rel"><span class="badge '+(ausp?'he':'tai')+'">'+y+'年'+d+'：'+info.name+'（'+info.label+'）</span></div>'
    +'<div class="ts-remedy" style="color:var(--text);font-size:14px;line-height:1.8">大門開在'+d+'，今年該方位飛入'+info.name+'（'+info.label+'）。<br><b style="color:var(--orange)">蘇民峰化解法：</b>'+r.treat+'</div>'
    +'<div class="ts-remedy" style="font-size:12px;color:var(--dim)">※ 依蘇民峰「大門地氈顏色旺宅化病方法」（通用推理體系，已按所選年份飛星方位即時推算）。</div>';
  fillGrid(document.getElementById('door-grid'),g,DIRS_CN,pos,false);
  document.getElementById('door-label').textContent=y+'年大門地氈法（'+STAR_DATA[c].name+'入中）';
}

/* ── 生肖收折 ── */
function toggleAll(open){document.querySelectorAll('details.zodiac-sec').forEach(d=>{open?d.setAttribute('open',''):d.removeAttribute('open')})}

/* ── 返回頂部 ── */
(function(){
  var btn=document.getElementById('toTop');
  if(!btn)return;
  var onScroll=function(){
    btn.classList.toggle('show',(window.pageYOffset||document.documentElement.scrollTop)>400);
  };
  window.addEventListener('scroll',onScroll,{passive:true});
  btn.addEventListener('click',function(){
    window.scrollTo({top:0,behavior:'smooth'});
  });
  onScroll();
})();

/* ── AR 方位模式（鏡頭 + 指南針：指向方位即見該方位之星／流年／化解）── */
var AR={on:false,stream:null,heading:0,raf:0,hasSensor:false};
var AR_DIRS=['北','東北','東','東南','南','西南','西','西北'];
var AR_POS={東南:[0,0],南:[0,1],西南:[0,2],東:[1,0],中宮:[1,1],西:[1,2],東北:[2,0],北:[2,1],西北:[2,2]};
var AR_OFF={北:0,東北:45,東:90,東南:135,南:180,西南:225,西:270,西北:315};
function arHeadingFromEvent(e){
  if(typeof e.webkitCompassHeading==='number')return e.webkitCompassHeading;   // iOS
  if(typeof e.alpha==='number')return ((360-e.alpha)%360+360)%360;           // Android（平放近似）
  return AR.heading;
}
function arSensorCb(e){AR.heading=arHeadingFromEvent(e);AR.hasSensor=true;}
function arSector(h){return Math.round((((h%360)+360)%360)/45)%8;}
function arDraw(){
  if(!AR.on)return;
  var y=+document.getElementById('fly-year').value;
  var g=getGrid(centerStar(y));
  var cv=document.getElementById('ar-canvas');
  var ctx=cv.getContext('2d');
  var W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
  var cx=W/2,cy=H/2,R=Math.min(W,H)*0.38;
  var d=AR_DIRS[arSector(AR.heading)];
  var star=g[AR_POS[d][0]][AR_POS[d][1]];
  var info=STAR_DATA[star];
  ctx.clearRect(0,0,W,H);
  // 八方位扇區
  for(var i=0;i<8;i++){
    var a0=(-90+i*45)*Math.PI/180,a1=(-90+(i+1)*45)*Math.PI/180;
    var s2=g[AR_POS[AR_DIRS[i]][0]][AR_POS[AR_DIRS[i]][1]];
    var col=STAR_DATA[s2].type==='danger'?'rgba(248,113,113,0.38)':STAR_DATA[s2].type==='inauspicious'?'rgba(251,146,60,0.35)':'rgba(74,222,128,0.30)';
    ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,R,a0,a1);ctx.closePath();
    ctx.fillStyle=col;ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.55)';ctx.lineWidth=1;ctx.stroke();
    var am=(a0+a1)/2;
    ctx.fillStyle='rgba(255,255,255,0.92)';ctx.font='bold 15px sans-serif';ctx.textAlign='center';
    ctx.fillText(AR_DIRS[i],cx+Math.cos(am)*(R*0.72),cy+Math.sin(am)*(R*0.72)+5);
    ctx.fillStyle='rgba(255,255,255,0.75)';ctx.font='12px sans-serif';
    ctx.fillText(STAR_DATA[s2].name,cx+Math.cos(am)*(R*0.42),cy+Math.sin(am)*(R*0.42)+4);
  }
  // 中宮
  ctx.beginPath();ctx.arc(cx,cy,R*0.22,0,Math.PI*2);
  ctx.fillStyle='rgba(108,140,255,0.30)';ctx.fill();
  ctx.strokeStyle='rgba(108,140,255,0.8)';ctx.stroke();
  ctx.fillStyle='#fff';ctx.font='bold 13px sans-serif';ctx.textAlign='center';
  ctx.fillText('中宮',cx,cy-2);ctx.font='12px sans-serif';
  ctx.fillText(STAR_DATA[g[1][1]].name,cx,cy+14);
  // 指向針（heading）
  var na=(-90+AR.heading)*Math.PI/180;
  ctx.beginPath();ctx.moveTo(cx,cy);
  ctx.lineTo(cx+Math.cos(na)*(R-8),cy+Math.sin(na)*(R-8));
  ctx.strokeStyle='#fff';ctx.lineWidth=3;ctx.stroke();
  ctx.beginPath();ctx.arc(cx,cy,5,0,Math.PI*2);ctx.fillStyle='#fff';ctx.fill();
  // 資訊卡
  var card=document.getElementById('ar-info');
  card.innerHTML='<div class="ar-dir">面向 '+d+'（'+AR_OFF[d]+'°）</div>'
    +'<div class="ar-star">'+info.name+' <span class="ar-lab">'+info.label+'</span></div>'
    +'<div class="ar-fortune">'+info.fortune+'</div>'
    +'<div class="ar-remedy">'+info.remedy+'</div>'
    +'<div class="ar-note">'+y+'年九宮 · '+STAR_DATA[centerStar(y)].name+'入中</div>';
  AR.raf=requestAnimationFrame(arDraw);
}
function startAR(){
  var ov=document.getElementById('ar-overlay');
  ov.classList.add('on');
  AR.on=true;
  if(!AR.sliderBound){
    AR.sliderBound=true;
    document.getElementById('ar-slider').addEventListener('input',function(){
      document.getElementById('ar-slider-val').textContent=this.value+'°';
      if(!AR.hasSensor)AR.heading=+this.value;
    });
  }
  // 指南針權限（iOS 13+）／感應器
  var perm=window.DeviceOrientationEvent&&window.DeviceOrientationEvent.requestPermission;
  var after=function(){
    window.addEventListener('deviceorientation',arSensorCb);
    window.addEventListener('deviceorientationabsolute',arSensorCb);
    AR.raf=requestAnimationFrame(arDraw);
  };
  if(perm){
    window.DeviceOrientationEvent.requestPermission().then(function(st){
      if(st==='granted')after();else{AR.hasSensor=false;after();}
    }).catch(function(){after();});
  }else after();
  arStartCam();
}
function arStartCam(){
  if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia){arSetCamLabel(false);return;}
  navigator.mediaDevices.getUserMedia({video:{facingMode:{ideal:'environment'}}}).then(function(s){
    AR.stream=s;
    var v=document.getElementById('ar-video');
    v.srcObject=s;v.play().catch(function(){});
    arSetCamLabel(true);
  }).catch(function(){arSetCamLabel(false);});
}
function arStopCam(){
  if(AR.stream){AR.stream.getTracks().forEach(function(t){t.stop()});AR.stream=null;}
  document.getElementById('ar-video').srcObject=null;
  arSetCamLabel(false);
}
function arToggleCam(){
  if(AR.stream){arStopCam();}else{arStartCam();}
}
function arSetCamLabel(on){
  var b=document.getElementById('ar-cam-toggle');
  if(!b)return;
  b.textContent=on?'📷 實景開':'📷 實景關';
  b.classList.toggle('off',!on);
}
function stopAR(){
  AR.on=false;
  cancelAnimationFrame(AR.raf);
  arStopCam();
  window.removeEventListener('deviceorientation',arSensorCb);
  window.removeEventListener('deviceorientationabsolute',arSensorCb);
  document.getElementById('ar-overlay').classList.remove('on');
}
