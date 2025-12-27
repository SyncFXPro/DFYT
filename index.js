
function site(){
const inp = document.createElement('input');
inp.classList.add('input');
inp.type = 'text';
inp.placeholder = 'Enter the URL';
document.body.appendChild(inp);

const select = document.createElement('select');
select.classList.add('select');
select.innerHTML = `
    <option value="video">Video</option>
    <option value="audio">Audio</option>
`;
document.body.appendChild(select);




const download = document.createElement('button');
download.classList.add('download');
download.innerText = 'Download';

download.addEventListener('click', async function() {
    const url = inp.value.trim();
    const type = select.value;
    
    if (!url) {
        alert("Please enter a URL");
        return;
    }
    

    
    // Disable button during download
    download.disabled = true;
    download.innerText = 'Downloading...';
    
    try {
        const response = await fetch('http://172.22.112.1:2847/download/v2', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                type: type
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Download failed');
        }
        
        // Extract filename from headers BEFORE converting to blob
        // Backend sends X-Filename header (see download.py line 82)
        let filename = null;
        
        // Try to get X-Filename header (case-insensitive check)
        for (const [key, value] of response.headers.entries()) {
            if (key.toLowerCase() === 'x-filename') {
                filename = value;
                break;
            }
        }
        
        // If not found, try Content-Disposition header
        if (!filename) {
            const contentDisposition = response.headers.get('Content-Disposition') || 
                                      response.headers.get('content-disposition');
            
            if (contentDisposition) {
                // Extract filename from Content-Disposition: attachment; filename="something.ext"
                const match = contentDisposition.match(/filename=["']?([^"';]+)["']?/i);
                if (match && match[1]) {
                    filename = match[1].trim();
                    // Handle URL-encoded filenames
                    try {
                        filename = decodeURIComponent(filename);
                    } catch (e) {
                        // If decoding fails, use as-is
                    }
                }
            }
        }
        
        // Fallback to default if still not found
        if (!filename) {
            filename = 'download'; 
        }
        
        console.log('Downloading file:', filename);
        
        // Get the blob and trigger browser download
        const blob = await response.blob();
        const blobUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = blobUrl;
        a.download = filename;
        
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(blobUrl);
        
        download.innerText = 'Download Complete!';
        setTimeout(function() {
            download.innerText = 'Download';
        }, 2000);
    } catch (error) {
        alert("Error: " + error.message);
        download.innerText = 'Download';
    } finally {
        download.disabled = false;
    }
});
document.body.appendChild(download);

}

site();