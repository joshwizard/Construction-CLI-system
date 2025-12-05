import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [output, setOutput] = useState([
    'Construction CLI Web Terminal',
    'Type "buildcli --help" to get started',
    'Special commands: "clear" to clear terminal, "exit" to close',
    ''
  ]);
  const [currentInput, setCurrentInput] = useState('');
  const [commandHistory, setCommandHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const inputRef = useRef(null);
  const terminalRef = useRef(null);

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [output]);

  const executeCommand = async (command) => {
    if (!command.trim()) return;

    // Handle special commands
    if (command.trim() === 'clear') {
      clearTerminal();
      return;
    }

    if (command.trim() === 'exit') {
      setOutput(prev => [...prev, `$ ${command}`, 'Goodbye! You can close this browser tab.']);
      setTimeout(() => {
        window.close();
      }, 1000);
      return;
    }

    // Add command to history
    setCommandHistory(prev => [...prev, command]);
    setHistoryIndex(-1);

    // Add command to output
    setOutput(prev => [...prev, `$ ${command}`]);

    try {
      // Simulate CLI execution (in real app, this would call your backend)
      const result = await simulateCliCommand(command);
      setOutput(prev => [...prev, ...result.split('\n').filter(line => line.trim())]);
    } catch (error) {
      setOutput(prev => [...prev, `Error: ${error.message}`]);
    }
  };

  const simulateCliCommand = async (command) => {
    // Mock CLI responses for demonstration
    const responses = {
      'buildcli --help': `Usage: buildcli [OPTIONS] COMMAND [ARGS]...

  Construction Management CLI System

Options:
  --help  Show this message and exit.

Commands:
  materials            Material management commands
  materials-add        Add a new material
  materials-inventory  Show inventory status
  materials-list       List all materials
  materials-order      Create a material order
  materials-orders     List all material orders
  materials-stock      Update material stock quantity
  materials-suppliers  Supplier management
  project              Project management commands
  project-create       Create a new project
  project-list         List all projects
  project-milestones   Project milestones management
  project-phases       Project phases management
  project-status       Show project status
  project-update       Update project details`,

      'buildcli project': `Usage: buildcli project [OPTIONS] COMMAND [ARGS]...

  Project management commands

Options:
  --help  Show this message and exit.

Commands:
  create      Create a new project
  list        List all projects
  milestones  Project milestones management
  phases      Project phases management
  status      Show project status
  update      Update project details`,

      'buildcli project --help': `Usage: buildcli project [OPTIONS] COMMAND [ARGS]...

  Project management commands

Commands:
  create      Create a new project
  list        List all projects
  milestones  Project milestones management
  phases      Project phases management
  status      Show project status
  update      Update project details`,

      'buildcli materials --help': `Usage: buildcli materials [OPTIONS] COMMAND [ARGS]...

  Material management commands

Commands:
  add        Add a new material
  inventory  Show inventory status
  list       List all materials
  suppliers  Supplier management`,

      'buildcli project list': `Project List:
1. Kitchen Renovation - $15,000 - active
2. Bathroom Remodel - $8,500 - active`,

      'buildcli materials list': `Materials List:
1. Concrete - cubic-yard - $120.00
2. Steel Rebar - ton - $800.00
3. Lumber - board-foot - $3.50`,

      'buildcli materials inventory': `Inventory Status:
Concrete: 50.0 cubic-yard - Location: Site A
Steel Rebar: 5.0 ton - Location: Warehouse B
Lumber: 0 board-foot - Location: N/A`,

      'buildcli materials': `Usage: buildcli materials [OPTIONS] COMMAND [ARGS]...

  Material management commands

Options:
  --help  Show this message and exit.

Commands:
  add        Add a new material
  inventory  Show inventory status
  list       List all materials
  order      Create a material order
  orders     List all material orders
  stock      Update material stock quantity
  suppliers  Supplier management`,

      'buildcli materials suppliers --help': `Usage: buildcli materials suppliers [OPTIONS] COMMAND [ARGS]...

  Supplier management

Options:
  --help  Show this message and exit.

Commands:
  add   Add a new supplier
  list  List all suppliers`,

      'buildcli project phases --help': `Usage: buildcli project phases [OPTIONS] COMMAND [ARGS]...

  Project phases management

Options:
  --help  Show this message and exit.

Commands:
  add   Add a phase to a project
  list  List phases for a project`,

      'buildcli project milestones --help': `Usage: buildcli project milestones [OPTIONS] COMMAND [ARGS]...

  Project milestones management

Options:
  --help  Show this message and exit.

Commands:
  add       Add a milestone to a project
  complete  Mark milestone as completed
  list      List milestones for a project`,

      // Flat command responses
      'buildcli project-create': `=== Create New Project ===
Project name: [Enter project name]
Budget (optional, press Enter to skip): [Enter budget or skip]
Start date YYYY-MM-DD (optional, press Enter to skip): [Enter date or skip]
Project location (optional, press Enter to skip): [Enter location or skip]

✅ Project created successfully!
Name: New Project
ID: 15
Budget: $50,000.00
Location: Construction Site
Start Date: 2024-01-15`,
      'buildcli project-list': `Project List:
1. Kitchen Renovation - $15,000 - active
2. Bathroom Remodel - $8,500 - active`,
      'buildcli project-status': 'Usage: buildcli project-status --project-id PROJECT_ID',
      'buildcli project-update': 'Usage: buildcli project-update --project-id PROJECT_ID [OPTIONS]',
      'buildcli project-phases': 'Usage: buildcli project-phases [OPTIONS] COMMAND [ARGS]...',
      'buildcli project-milestones': 'Usage: buildcli project-milestones [OPTIONS] COMMAND [ARGS]...',
      'buildcli materials-add': `=== Add New Material ===
Material name: [Enter material name]
Unit of measurement (e.g., cubic-yard, ton, piece): [Enter unit]
Cost per unit: [Enter cost]
Supplier name (optional, press Enter to skip): [Enter supplier or skip]

✅ Material added successfully!
Name: New Material
ID: 42
Unit: piece
Cost per unit: $25.00`,
      'buildcli materials-list': `Materials List:
1. Concrete - cubic-yard - $120.00
2. Steel Rebar - ton - $800.00
3. Lumber - board-foot - $3.50`,
      'buildcli materials-inventory': `Inventory Status:
Concrete: 50.0 cubic-yard - Location: Site A
Steel Rebar: 5.0 ton - Location: Warehouse B
Lumber: 0 board-foot - Location: N/A`,
      'buildcli materials-stock': `=== Update Stock ===
Available materials:
  1. Concrete (cubic-yard)
  2. Steel Rebar (ton)
  3. Lumber (board-foot)

Enter material ID: [Select material]
Enter quantity: [Enter amount]
Storage location: [Enter location]

✅ Stock updated successfully!
Material: Concrete
Quantity: 100.0 cubic-yard
Location: Site A`,
      'buildcli materials-order': `=== Create Material Order ===
Available materials:
  1. Concrete (cubic-yard) - $120.00
  2. Steel Rebar (ton) - $800.00
  3. Lumber (board-foot) - $3.50

Enter material ID: [Select material]
Enter quantity: [Enter amount]
Available suppliers:
  1. ABC Supply Co - 555-0123
  2. BuildMart - buildmart@email.com

Enter supplier ID: [Select supplier]
Delivery date (YYYY-MM-DD, optional): [Enter date or skip]

✅ Order created successfully!
Order ID: 7
Material: Concrete
Quantity: 50.0 cubic-yard
Supplier: ABC Supply Co
Total Cost: $6,000.00
Expected Delivery: 2024-02-15`,
      'buildcli materials-orders': `Material Orders:
1. Concrete - 100.0 cubic-yard - ABC Supply Co - $12,000.00 - pending - Delivery: 2024-02-15
2. Steel Rebar - 5.0 ton - Steel Works - $4,000.00 - pending - Delivery: 2024-03-01`,
      'buildcli materials-suppliers': 'Usage: buildcli materials-suppliers [OPTIONS] COMMAND [ARGS]...'
    };

    // Check for create commands
    if (command.startsWith('buildcli project create')) {
      const match = command.match(/create "([^"]+)"/);
      const projectName = match ? match[1] : 'New Project';
      return `Created project: ${projectName} (ID: ${Math.floor(Math.random() * 100)})
Budget: $50,000.00`;
    }

    if (command.startsWith('buildcli materials add')) {
      const match = command.match(/add "([^"]+)"/);
      const materialName = match ? match[1] : 'New Material';
      return `Added material: ${materialName} (ID: ${Math.floor(Math.random() * 100)})
Unit: piece
Cost per unit: $10.00`;
    }

    if (command.startsWith('buildcli materials suppliers')) {
      if (command.includes('add')) {
        const match = command.match(/add "([^"]+)"/);
        const supplierName = match ? match[1] : 'New Supplier';
        return `Added supplier: ${supplierName} (ID: ${Math.floor(Math.random() * 100)})
Contact: 555-0123`;
      }
      if (command.includes('list')) {
        return `Suppliers List:
1. ABC Supply Co - 555-0123
2. BuildMart - buildmart@email.com
3. Steel Works - steel@works.com`;
      }
    }

    if (command === 'buildcli materials orders') {
      return `Material Orders:
1. Concrete - 100.0 cubic-yard - ABC Supply Co - $12,000.00 - pending - Delivery: 2024-02-15
2. Steel Rebar - 5.0 ton - Steel Works - $4,000.00 - pending - Delivery: 2024-03-01`;
    }

    if (command.startsWith('buildcli project phases')) {
      if (command.includes('add')) {
        const match = command.match(/add "([^"]+)"/);
        const phaseName = match ? match[1] : 'New Phase';
        return `Added phase: ${phaseName} (ID: ${Math.floor(Math.random() * 100)}) to project Kitchen Renovation
Duration: 30 days`;
      }
      if (command.includes('list')) {
        return `Phases for project: Kitchen Renovation
1. Foundation - 30 days - planned
2. Framing - 45 days - planned
3. Finishing - 60 days - planned`;
      }
    }

    if (command.startsWith('buildcli project milestones')) {
      if (command.includes('add')) {
        const match = command.match(/add "([^"]+)"/);
        const milestoneName = match ? match[1] : 'New Milestone';
        return `Added milestone: ${milestoneName} (ID: ${Math.floor(Math.random() * 100)}) to project Kitchen Renovation
Target date: 2024-06-01`;
      }
      if (command.includes('list')) {
        return `Milestones for project: Kitchen Renovation
1. Foundation Complete - Target: 2024-02-15 - Status: completed
2. Roof Installation - Target: 2024-04-30 - Status: pending
3. Grand Opening - Target: 2024-08-01 - Status: pending`;
      }
      if (command.includes('complete')) {
        return `Milestone 'Foundation Complete' marked as completed`;
      }
    }

    return responses[command] || `Command not recognized: ${command}
Try "buildcli --help" for available commands`;
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      executeCommand(currentInput);
      setCurrentInput('');
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (commandHistory.length > 0) {
        const newIndex = historyIndex === -1 ? commandHistory.length - 1 : Math.max(0, historyIndex - 1);
        setHistoryIndex(newIndex);
        setCurrentInput(commandHistory[newIndex]);
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex !== -1) {
        const newIndex = historyIndex + 1;
        if (newIndex >= commandHistory.length) {
          setHistoryIndex(-1);
          setCurrentInput('');
        } else {
          setHistoryIndex(newIndex);
          setCurrentInput(commandHistory[newIndex]);
        }
      }
    }
  };

  const clearTerminal = () => {
    setOutput([
      'Construction CLI Web Terminal', 
      'Type "buildcli --help" to get started',
      'Special commands: "clear" to clear terminal, "exit" to close',
      ''
    ]);
  };

  return (
    <div className="App">
      <div className="header">
        <h1>🏗️ Construction CLI Web Terminal</h1>
        <button onClick={clearTerminal} className="clear-btn">Clear</button>
      </div>
      
      <div className="terminal" ref={terminalRef}>
        {output.map((line, index) => (
          <div key={index} className="terminal-line">
            {line}
          </div>
        ))}
        
        <div className="input-line">
          <span className="prompt">$ </span>
          <input
            ref={inputRef}
            type="text"
            value={currentInput}
            onChange={(e) => setCurrentInput(e.target.value)}
            onKeyDown={handleKeyDown}
            className="terminal-input"
            placeholder="Type buildcli commands here..."
          />
        </div>
      </div>

      <div className="help-panel">
        <h3>Quick Commands:</h3>
        <div className="command-examples">
          <button onClick={() => setCurrentInput('buildcli --help')}>buildcli --help</button>
          <button onClick={() => setCurrentInput('buildcli project-list')}>buildcli project-list</button>
          <button onClick={() => setCurrentInput('buildcli materials-list')}>buildcli materials-list</button>
          <button onClick={() => setCurrentInput('buildcli materials-inventory')}>buildcli materials-inventory</button>
          <button onClick={() => setCurrentInput('buildcli project-create')}>buildcli project-create</button>
          <button onClick={() => setCurrentInput('buildcli project create "My Project" --budget 100000')}>Create Project</button>
          <button onClick={() => setCurrentInput('clear')} className="special-cmd">clear</button>
          <button onClick={() => setCurrentInput('exit')} className="exit-cmd">exit</button>
        </div>
      </div>
    </div>
  );
}

export default App;