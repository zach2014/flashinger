from flask import render_template
from uimgmt import app
from uimgmt.models import DockerMachine, MacVlanInterface
import docker

@app.route('/')
def home_page():
    machines = DockerMachine.query.all()
    return render_template("home.html", machines=machines)


@app.route('/machine/<machine_id>')
def show_machine(machine_id):
    machine = DockerMachine.query.get(machine_id)
    if machine:
        api_url = 'tcp://{}:2376'.format(machine.ip_addr)
        client = docker.DockerClient(base_url=api_url)
        try:
            version = client.version()
            containers = client.containers.list()
            networks = client.networks.list()
            return render_template("machine.html", version=version, containers=containers, networks=networks)
        except Exception as e :
            return render_template("exception.html", error=e)
    else:
        return render_template('exception.html', error='Not found the resource')



@app.route('/interface/<interface_id>')
def show_interface(interface_id):
    intf =  MacVlanInterface.query.get(interface_id)
    if intf:
        return render_template('interface.html', intf=intf)
    else:
        return render_template('exception.html', error="Not find the resource")
