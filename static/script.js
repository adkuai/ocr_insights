document.getElementById('uploadBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('fileInput');
    const loader = document.getElementById('loader');
    const pdfContent = document.getElementById('pdfContent');
    const metaTableBody = document.getElementById('metaTableBody');
    const itemsTableBody = document.getElementById('itemsTableBody');
    
    if (!fileInput.files || fileInput.files.length === 0) {
        return alert('Please upload a valid document first.');
    }
    
    // Hide components and scrub grid records instantly on click
    pdfContent.style.display = 'none';
    metaTableBody.innerHTML = '';
    itemsTableBody.innerHTML = '';
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    // Unveil moving loading spinner elements
    loader.style.display = 'block';
    
    try {
        const res = await fetch('/analyze', { method: 'POST', body: formData });
        const json = await res.json();
        
        if (json.status === "success" && json.data) {
            const docData = json.data;
            
            // Map Language Code to Full Readable Name
            let languageDisplay = docData.language;
            if (docData.language) {
                const langLower = docData.language.toLowerCase().trim();
                if (langLower === 'en') languageDisplay = 'English';
                else if (langLower === 'hi') languageDisplay = 'Hindi';
                else if (langLower === 'mixed') languageDisplay = 'English + Hindi';
            }

            // Map General Metadata Data Rows
            const fieldsToDisplay = [
                { label: 'Document Type', value: docData.document_type },
                { label: 'Language Detected', value: languageDisplay }, // <-- Uses the cleaned name
                { label: 'Document Title', value: docData.document_title },
                { label: 'Date', value: docData.date },
                { label: 'Document Number', value: docData.document_number },
                { label: 'Organization Name', value: docData.organization_name },
                { label: 'Subtotal Amount', value: docData.subtotal },
                { label: 'Tax Amount', value: docData.tax },
                { label: 'Total Amount', value: docData.total_amount ? `${docData.total_amount} ${docData.currency || ''}`.trim() : null },
                { label: 'Model Confidence', value: docData.confidence }
            ];

            fieldsToDisplay.forEach(field => {
                const row = `<tr>
                    <td><strong>${field.label}</strong></td>
                    <td>${field.value !== null && field.value !== undefined ? field.value : '<span style="color: #94a3b8;">N/A</span>'}</td>
                </tr>`;
                metaTableBody.innerHTML += row;
            });

            // Map Line Items
            if (docData.items && docData.items.length > 0) {
                docData.items.forEach(item => {
                    const row = `<tr>
                        <td style="font-weight: 600; color: #1e293b;">${item.name || '<span style="color: #94a3b8;">N/A</span>'}</td>
                        <td>${item.quantity !== null && item.quantity !== undefined ? item.quantity : '-'}</td>
                        <td>${item.unit || '-'}</td>
                        <td>${item.unit_price !== null && item.unit_price !== undefined ? item.unit_price : '-'}</td>
                        <td><strong>${item.amount !== null && item.amount !== undefined ? item.amount : '-'}</strong></td>
                    </tr>`;
                    itemsTableBody.innerHTML += row;
                });
            } else {
                itemsTableBody.innerHTML = `<tr><td colspan="5" style="text-center; color: #94a3b8; padding: 1.5rem; text-align: center;">No line items detected.</td></tr>`;
            }
            
            // Bring the report card dynamically into view
            pdfContent.style.display = 'block';
        } else {
            alert('Processing complete but data fields returned empty.');
        }
    } catch (err) {
        alert('Server processing error: ' + err.message);
    } finally {
        // Natively turn off the animation loader
        loader.style.display = 'none';
    }
});
