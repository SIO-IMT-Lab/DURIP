        async function executeCommand(command, args) {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    "command": command, 
                    "args": args }),
            });
            const result = await response.text();
        }

        function addSchedule(event) {
            event.preventDefault();
            const form = event.target;
            const sensor = form.sensor.value;
            const start = form.start.value;
            const end = form.end.value;
            const state = form.state.value;
            const repeat = form.repeat.checked ? 'true' : '';
            const days = Array.from(form.days.selectedOptions).map(option => option.value).join(',');
            const endRepeat = form.endRepeat.value;
            const args = [sensor, start, end, state, repeat, days, endRepeat].filter(arg => arg !== '').join(',');
            executeCommand('add', args);
            viewSchedules();
        }

        function removeSchedule(event) {
            event.preventDefault();
            const form = event.target;
            const sensor = form.sensor.value;
            const index = form.index.value;
            executeCommand('remove', `${sensor},${index}`);
            viewSchedules();
        }

        function overrideSensor(event) {
            event.preventDefault();
            const form = event.target;
            const sensor = form.sensor.value;
            const state = form.state.value;
            executeCommand('override', `${sensor},${state}`);
            viewSchedules();
            viewStates();
        }

        function removeOverride(event) {
            event.preventDefault();
            const sensor = event.target.sensor.value;
            executeCommand('remove_override', sensor);
            viewSchedules();
            viewStates();
        }

        function viewSchedules() {
            fetch('/view_schedules').then(response => response.text()).then(text => {
                document.getElementById('result').textContent = text;
            }
            );
        }

        function viewStates() {
            fetch('/view_states').then(response => response.text()).then(text => {
                document.getElementById('current').textContent = text;
            }
            );
        }

        setInterval(viewStates, 2000);

        document.addEventListener('DOMContentLoaded', function() {
            viewSchedules();
            viewStates();

            document.getElementById('uploadForm').onsubmit = async function(event) {
                event.preventDefault(); // Prevent the form from submitting the traditional way
        
                const fileInput = document.getElementById('jsonFile');
                const file = fileInput.files[0];
        
                if (!file || file.type !== "application/json") {
                    alert("Please select a valid JSON file.");
                    return;
                }
        
                try {
                    const text = await file.text();
                    JSON.parse(text); // Try parsing the file text as JSON
        
                    // If parsing succeeds, submit the form data using Fetch API or handle the file as needed
                    const formData = new FormData();
                    formData.append("file", file);
        
                    const response = await fetch('/upload_schedule/', {
                        method: 'POST',
                        body: formData,
                    });
        
                    if (response.ok) {
                        alert("File uploaded successfully!");
                    } else {
                        alert("Failed to upload the file.");
                    }
                } catch (error) {
                    // If parsing fails, it's not a valid JSON file
                    alert("The file is not a valid JSON.");
                }
            };
        });