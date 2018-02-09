from flask import render_template,redirect, url_for, request, flash
from uimgmt import app, db
from uimgmt.models import DockerMachine, MacVlanInterface
from uimgmt.forms import MachineForm, InterfaceForm, UpgraderServiceForm
import docker

@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/machine/')
def show_machine():
    return render_template("machine.html",
            m_form=MachineForm(), 
            machines=DockerMachine.query.all())


@app.route('/machine/add', methods=['POST'])
def add_machine():
    if request.method == 'POST':
        m_form = MachineForm(request.form)
        if m_form.validate():
            machine = DockerMachine()
            m_form.populate_obj(machine)
            db.session.add(machine)
            db.session.commit()
            flash('Add new machine successfully!')
        else:
            flash('Error: {}'.format(m_form.errors))

        return redirect(url_for('show_machine'))


@app.route('/machine/del/<int:machine_id>')
def del_machine(machine_id):
    #DockerMachine.query.filter_by(id=machine_id).delete()
    m = DockerMachine.query.get(machine_id)
    if m:
        for intf in m.interfaces.all():
            intf.labels.clear()

        m.labels.clear()
        db.session.delete(m)
        db.session.commit()
    return redirect(url_for('show_machine'))


@app.route('/interface/')
def show_interface():
    return render_template('interface.html', 
            s_form=UpgraderServiceForm(),
            intfs=MacVlanInterface.query.all())


@app.route('/interface/add', methods=['POST'])
def add_interface():
    i_form = InterfaceForm(request.form)
    if request.method == 'POST':
        if i_form.validate():
            intf = MacVlanInterface()
            i_form.populate_obj(intf)
            db.session.add(intf)
            db.session.commit()
            flash('Add new interface successfuly')
        else:
            flash('Error: {}'.format(i_form.errors))
        return  redirect(url_for('show_machine'))


@app.route('/dockerd/<int:machine_id>')
def show_dockerd(machine_id):
    machine = DockerMachine.query.get(machine_id)
    if machine:
        api_url = 'tcp://{}:2376'.format(machine.ip_addr)
        client = docker.DockerClient(base_url=api_url)
        try:
            version = client.version()
            containers = client.containers.list()
            networks = client.networks.list()
            return render_template("dockerd.html",
                    version=version,
                    containers=containers,
                    networks=networks)
        except Exception as e :
            return render_template("exception.html", error=e)
    else:
        return render_template('exception.html', error='Not found the resource')


@app.route('/add_service', methods=['POST'])
def add_service():
    s_form = UpgraderServiceForm(request.form) 
    if request.method == 'POST':
        if s_form.validate():
           intf_id = s_form.intf_id.data()
           intf = MacVlaninterface.query.get(intf_id)
           machine = DockerMachine.query.get(intf.machine_id)
           dockerd_url= 'tcp://{0}:2376'.format(machine.ip_addr)
           msg = 'Add service on {0}'.format(dockerd_url)
        #flash('Add service...')
           flash(msg)
    return redirect(url_for('show_interface'))
